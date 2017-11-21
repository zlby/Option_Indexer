import tensorflow as tf
import os
import tensorflow.contrib.distributions as dst
import numpy as np

class LstmModel:
    def __init__(self, series, time_step=10, batch_size=10, cell_size=100):
        scale = np.std(np.multiply(series, 2.0), dtype=np.float32)
        self.__nmFunc = dst.Normal(loc=np.mean(series, 0, np.float32), scale=scale)
        self.__meta_list = series
        self.__input_size = 1
        self.__output_size = 1
        self.__forget_bias = 0.2
        self.__batch_size = batch_size
        self.__cell_size = cell_size
        self.__time_step = time_step
        self.cursor = 0
        self.__labels = None
        self.__batches = None
        self.__input_layer_var = None
        self.__cell_state = None
        self.__out_state = None
        self.__predication = None
        self.__last_out = None
        self.__input_placeholder = tf.placeholder(dtype=tf.float32, name="Inputs")
        self.__label_placeholder = tf.placeholder(dtype=tf.float32, name="labels")

        self.__predication = np.asarray([])
        self.__generate_next_batch()

        # Flags
        self.trained = False
        self.config = tf.ConfigProto(device_count={"CPU": 3},  # limit to num_cpu_core CPU usage
                                     inter_op_parallelism_threads=1,
                                     intra_op_parallelism_threads=1,
                                     log_device_placement=False
                                     )
        self.__session_holder = None

    def __get_input_layer_output(self):
        """A full-link layer"""
        with tf.name_scope("Input_Layer"):
            origin_in_x = tf.reshape(tensor=self.__input_placeholder,
                                     shape=[-1, self.__input_size]
                                     )
            l_in_x = self.__nmFunc.cdf(origin_in_x)
            Ws_in = tf.get_variable("input_layer_weights",
                                    shape=[self.__input_size, self.__cell_size],
                                    dtype=tf.float32
                                    )
            b_in = tf.get_variable("input_layer_bias",
                                   shape=[self.__cell_size]
                                   )
            self.__input_layer_var = (Ws_in, b_in)
            l_out = tf.add(
                tf.matmul(l_in_x, Ws_in),
                b_in
            )
            return tf.reshape(tensor=l_out,
                              shape=[self.__batch_size, self.__time_step, self.__cell_size],
                              name="input_layer_out"
                              )

    def __get_cell_layer_output(self, input_tensor):
        with tf.name_scope("Cell_Layer"):
            cell = tf.nn.rnn_cell.LSTMCell(num_units=self.__cell_size,
                                           activation=tf.tanh,
                                           forget_bias=self.__forget_bias
                                           )
            self.__cell_state = cell.zero_state(batch_size=self.__batch_size, dtype=tf.float32)
            cell_outputs, self.__out_state = tf.nn.dynamic_rnn(cell=cell,
                                                               inputs=input_tensor,
                                                               initial_state=self.__cell_state)
            return cell_outputs

    def __get_output_layer_output(self, input_tensor):
        with tf.name_scope("Output_Layer"):
            l_out_x = tf.reshape(input_tensor, shape=[-1, self.__cell_size])
            Ws_out = tf.get_variable(name="output_layer_weights",
                                     shape=[self.__cell_size, self.__output_size],
                                     dtype=tf.float32)
            bs_out = tf.get_variable(name="output_layer_bias", shape=[self.__output_size])

            l_out = tf.add(
                tf.matmul(
                    l_out_x,
                    Ws_out
                ),
                bs_out
            )
            return tf.reshape(tensor=l_out,
                              shape=[self.__batch_size, self.__time_step, self.__output_size],
                              name="output_layer_out"
                              )

    def __forward(self):
        """Forward calculate, fetch [self.input_placeholders] as input layer's input.

        :return l_out_o [Tensor]
            Predicate of give
        """
        l_in_o = self.__get_input_layer_output()
        l_c_o = self.__get_cell_layer_output(l_in_o)
        l_out_o = self.__get_output_layer_output(l_c_o)
        return l_out_o

    def __generate_train_step(self):
        l_out_o = self.__forward()
        self.pred = self.__nmFunc.quantile(l_out_o)
        _pred = tf.reshape(tensor=l_out_o,
                           shape=[-1],
                           name="predication"
                           )
        origin_labels = tf.reshape(tensor=self.__label_placeholder,
                                   shape=[-1],
                                   name="labels"
                                   )
        labels = self.__nmFunc.cdf(origin_labels)
        self.loss = tf.reduce_mean(tf.square(_pred - labels))
        self.train_step = tf.train.AdamOptimizer(0.01).minimize(self.loss)

    def __generate_next_batch(self):
        """generate next train batch."""
        # reset batch
        if self.__labels is not None:
            self.__batches = self.__labels
        self.__labels = None
        for i in range(self.__batch_size):
            self.__split_series()

    def __split_series(self):
        """fetch one train data"""
        sle = self.__meta_list[self.cursor: self.cursor + self.__time_step]
        self.__add_batch_data(
            sle[np.newaxis, :]

        )
        self.cursor += 1

    def __add_batch_data(self, data_element):
        """append one train data element to batch."""
        if self.__labels is not None:
            self.__labels = np.append(self.__labels, data_element, 0)
        else:
            self.__labels = data_element

    def __check_is_not_end(self):
        if self.__labels.shape[0] != self.__batch_size:
            return False
        return self.cursor < (self.__meta_list.shape[0] - self.__batch_size * self.__time_step)

    def train_till_series_end(self):
        self.__generate_train_step()
        if not self.__session_holder:
            self.__session_holder = tf.Session(config=self.config)
        sess = self.__session_holder
        sess.run(tf.global_variables_initializer())
        self.__generate_next_batch()
        _, state, prd = sess.run([self.train_step, self.__out_state, self.pred],
                                 feed_dict={self.__input_placeholder: self.__batches,
                                            self.__label_placeholder: self.__labels}
                                 )
        self.__predication = np.append(self.__predication, np.reshape(prd[0, :, 0], [-1]), 0)
        self.__predication = np.append(self.__predication, np.reshape(prd[1:, -1, 0], [-1]), 0)
        while self.__check_is_not_end():
            self.__generate_next_batch()
            loss, _, state, prd = sess.run([self.loss, self.train_step, self.__out_state, self.pred],
                                           feed_dict={self.__input_placeholder: self.__batches,
                                                      self.__label_placeholder: self.__labels,
                                                      self.__cell_state: state
                                                      })
            self.__predication = np.append(self.__predication, np.reshape(prd[:, -1, 0], [-1]), 0)
            if self.cursor % 20 == 0:
                print("run %s times: %s" % (self.cursor, loss))
        self.__last_out = (state, prd)

    def get_prediction_list(self):
        return self.__predication

    def predict(self, day_length):
        # with self.__session_holder as sess:
        if self.__session_holder is None:
            self.train_till_series_end()
        sess = self.__session_holder
        for i in range(day_length):
            self.__last_out = (sess.run([self.__out_state, self.pred], feed_dict={
                self.__input_placeholder: self.__last_out[1],
                self.__cell_state: self.__last_out[0]
            }))
            self.__predication = np.append(self.__predication,
                                           np.reshape(self.__last_out[1][:, -1, 0], [-1]), 0)
        return self.__predication[-day_length:]

    def close(self):
        """
        Must manually close!!!!!!!!
        :return:
        """
        self.__session_holder.close()
