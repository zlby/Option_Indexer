import tensorflow as tf
import tensorflow.contrib.distributions as dst
import numpy as np


def find_interval(value, avg, scale):
    with tf.name_scope("find_interval_with_raw_value"):
        min_of_interval = avg - tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale
        max_of_interval = avg + tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale
    return min_of_interval, max_of_interval


# move graph building in a function
class SubGraph(object):

    def __preprocessing_inputs(self, sample_size: int):
        with tf.name_scope('Input'):

            self.inputs = tf.placeholder(tf.float32, shape=[4, sample_size], name='Inputs')

            self.difference_vol = tf.subtract(self.inputs[1], self.inputs[0], name="Difference of vol")

            self.difference_price = tf.subtract(self.inputs[3], self.inputs[2], name="Difference of price")
            with tf.name_scope('Frequency'):
                difference_vol_sorted = tf.cast(tf.nn.top_k(self.difference_vol, sample_size).values,
                                                tf.float32,
                                                name="difference_vol_sorted")
                dr_frq = tf.div(
                    tf.convert_to_tensor([x for x in range(difference_vol_sorted.shape[0], 0, -1)],
                                         dtype=tf.float32,
                                         name="counts"),
                    difference_vol_sorted.shape[0].value,
                    name="Frequency"
                )
                tf.summary.histogram("sample_frequency", dr_frq)
        return difference_vol_sorted, dr_frq

    # fixme : assert tuple likes (Tensor, Tensor)
    def simulate_regular_normal_distribution_arguments(self, sample: tuple):
        with tf.name_scope("reg_norm_prediction"):
            avg = tf.reduce_mean(self.difference_vol)
            scl = tf.Variable(np.random.rand(), dtype=tf.float32)
            tf.summary.scalar("scl", self.scl)
            pdt_nm_dst = dst.Normal(loc=self.avg, scale=self.scl)

            # Evaluate dr , return the predicate frequency 1-D tensor
            pdt_frq = pdt_nm_dst.cdf(sample[0])

            with tf.name_scope("loss"):
                loss = tf.reduce_mean(tf.square((pdt_frq - sample[1]), name="error"), name="loss")
                tf.summary.scalar("loss", loss)

            with tf.name_scope("train"):
                self.train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

    def build_graph(self, sample_size):
        with tf.Graph().as_default() as self.g:
            sample_values, sample_frq = self.__preprocessing_inputs(sample_size)

            with tf.name_scope("reg_norm_prediction"):
                self.avg = tf.reduce_mean(self.difference_vol)
                self.scl = tf.Variable(np.random.rand(), dtype=tf.float32)
                tf.summary.scalar("scl", self.scl)
                pdt_nm_dst = dst.Normal(loc=self.avg, scale=self.scl)

                # Evaluate dr , return the predicate frequency 1-D tensor
                pdt_frq = pdt_nm_dst.cdf(sample_values)

                with tf.name_scope("loss"):
                    loss = tf.reduce_mean(tf.square((pdt_frq - sample_frq), name="error"), name="loss")
                    tf.summary.scalar("loss", loss)

                with tf.name_scope("train"):
                    self.train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

            with tf.name_scope("thresholds"):
                with tf.name_scope("init"):
                    # the thresholds to position or liquidate
                    # the _thresholds is to calculate the real threshold,
                    # cause thresholds should be in ascending order
                    # thresholds should be an 3-D tensor
                    # when over 2nd threshold to position and below 1st threshold to liquidate
                    # anytime when over 3rd threshold should show hand , and throwing an error.
                    # That's means the model should be retrained.
                    self._thresholds = tf.Variable(np.random.rand(3), dtype=tf.float32, name="_thresholds")
                    tf.summary.histogram("tsd_var", self._thresholds)
                    # Fixed: want to return the value of the PDFunction when key equals avg, maybe wrong?

                    self.max_raw_p = pdt_nm_dst.prob(self.avg)
                    self.dr_raw_p = pdt_nm_dst.prob(self.difference_vol)
                    self.dr_prob = pdt_nm_dst.prob(self.difference_vol, name="dr_prob")
                    # former_dr_prob = pdt_nm_dst.prob(former_dr)

                    # Get _thresholds latest snapshot values
                    self._thresholds_values = dst.Logistic(0., 3.).cdf(self._thresholds.value())
                    self.trd_nm = self.max_raw_p * self._thresholds_values[0]
                    self.trd_hg = self.trd_nm * self._thresholds_values[1]
                    self.trd_err = self.trd_hg * self._thresholds_values[2]

                    # solved : correctly get its value?
                    self.interval_nm = find_interval(self.trd_nm, self.avg, self.scl.value())
                    self.interval_hg = find_interval(self.trd_hg, self.avg, self.scl.value())
                    self.interval_err = find_interval(self.trd_err, self.avg, self.scl.value())

                self._logistic_cvt = dst.Logistic(loc=self.trd_hg, scale=0.1)
                self._logistic_sgn = dst.Logistic(loc=0., scale=0.1)
                # _logistic_diff = dst.Logistic(loc=0., scale=0.01)

                # for i in range(sample_size)[1:]:
                #     dr_change=_logistic_cvt.cdf(_logistic_cvt.cdf(dr_prob[i-1])*_logistic_cvt.cdf(dr_prob[i]))
                #     dr_sgn=

                with tf.name_scope("line_Layer_hg"):
                    self.dr_sgn = self._logistic_sgn.cdf(self.difference_vol) * 2. - 1.
                    self.out_hg = (1 - self._logistic_cvt.cdf(self.dr_prob)) * (self.difference_price * self.dr_sgn
                                                                                * 100 - 20)\
                             # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

                with tf.name_scope("line_Layer_nm"):
                    self.out_nm = (-self._logistic_cvt.cdf(self.dr_prob)) *(self.difference_price * self.dr_sgn
                                                                            * 100 - 20)
                             # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

                with tf.name_scope("threshold_summary"):
                    self.bene = tf.reduce_sum(tf.add(self.out_hg, self.out_nm), name="Benefits")
                    self.bene_cvt_to_limited_interval = dst.Logistic(0., 5.).cdf(-self.bene)
                    self.trd_train = tf.train.AdamOptimizer(1e-6).minimize(self.bene_cvt_to_limited_interval)

            self.init = tf.global_variables_initializer()

            # CREATE MODEL STRUCTURE SEND #
        return self
