import tensorflow as tf
import numpy as np
import pylab as pl

TIME_STEP = 10
BATCH_SIZE = 20
INPUT_SIZE = OUTPUT_SIZE = 1
CELL_SIZE = 10
START = 0

def get_batch():
    global START
    _xs = np.arange(START, START + BATCH_SIZE * (TIME_STEP + 1)).reshape((BATCH_SIZE, (TIME_STEP + 1)))
    data = np.sin(_xs * np.pi / 10) + np.sin(_xs * np.pi / 17)
    START += BATCH_SIZE * TIME_STEP
    return _xs[:, :-1, np.newaxis], data[:, 1:, np.newaxis], data[:, :-1, np.newaxis], _xs[-1,-1], data[-1,-1]


xs = tf.placeholder(tf.float32, [None, TIME_STEP, INPUT_SIZE], name="xs")
ys = tf.placeholder(tf.float32, [None, TIME_STEP, OUTPUT_SIZE], name="ys")

with tf.name_scope("input_layer"):
    _xs = tf.reshape(xs, [-1, INPUT_SIZE])
    Ws_in = tf.get_variable("input_weights", [INPUT_SIZE, CELL_SIZE])
    b_in = tf.get_variable("input_bias", [CELL_SIZE])
    l_in_x = tf.reshape(tf.add(tf.matmul(_xs, Ws_in), b_in), [BATCH_SIZE, TIME_STEP, CELL_SIZE])

with tf.name_scope("expand_cells"):
    cell = tf.nn.rnn_cell.LSTMCell(CELL_SIZE)
    init_state = cell.zero_state(BATCH_SIZE, dtype=tf.float32)
    cell_outputs, cell_states = tf.nn.dynamic_rnn(cell, l_in_x, initial_state=init_state)

with tf.name_scope("output_layer"):
    l_out_x = tf.reshape(cell_outputs, [-1, CELL_SIZE])
    Ws_out = tf.get_variable("output_weights", [CELL_SIZE, OUTPUT_SIZE])
    b_out = tf.get_variable("output_bias", [OUTPUT_SIZE])
    pred = tf.add(tf.matmul(l_out_x, Ws_out), b_out)

with tf.name_scope("train"):
    _ys = tf.reshape(ys, [-1])
    _pred = tf.reshape(pred, [-1])
    loss = tf.reduce_mean(tf.square(tf.subtract(_ys, _pred)))
    train_step = tf.train.AdamOptimizer(0.01).minimize(loss)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)

    x_l, y_l, p_l = [], [], []

    for i in range(200):
        xaxs, _data, _label, value_x, value_y = get_batch()
        if i == 0:
            feed_dict = {
                xs: _data,
                ys: _label
            }
        else:
            feed_dict = {
                xs: _data,
                ys: _label,
                init_state: state
            }

        _, cost, state, prd = sess.run([train_step, loss, cell_states, pred], feed_dict=feed_dict)
        x_l.append(value_x)
        y_l.append(value_y)
        p_l.append(prd[-1,-1])

        if i % 20 == 0:
            print("cost: ", round(cost, 4))

    pl.plot(x_l, y_l)
    pl.plot(x_l, p_l)
    pl.show()