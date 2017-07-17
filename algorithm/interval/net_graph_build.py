# import data
# import algorithm.database_link as dl
# import algorithm.interval.data
import tensorflow as tf
import tensorflow.contrib.distributions as dst
import numpy as np


# r1 = data.get_first_rate_list()
# r2 = data.get_second_rate_list()
#
# p1 = data.get_first_price_list()
# p2 = data.get_second_price_list()

# sample_size = len(r1)

# CREATE MODEL STRUCTURE START #

# Create normal predicate layer


def find_interval(value, avg, scale):
    return (avg - tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale,
            avg + tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale)


# move graph building in a function
class SubGraph(object):
    def __init__(self):
        self.build_graph()

    def build_graph(self):
        with tf.Graph().as_default() as self.g:
            with tf.name_scope('Input'):
                # fixme : resolve sample_size
                self.inputs = tf.placeholder(tf.float32, shape=[4, 8640], name='inputs')
                # nm_args = tf.Variable(tf.zeros([2], tf.float32, name="normal arguments"))
                self.dr = tf.subtract(self.inputs[1], self.inputs[0], name="dr")
                # former_dr = ([0]+dr)[0:sample_size]  # TODO change

                self.dp = tf.subtract(self.inputs[3], self.inputs[2], name="dp")
                with tf.name_scope('frequency'):
                    self.dr_sorted = tf.cast(tf.nn.top_k(self.dr, 8640).values, tf.float32, name="dr_sorted")
                    self.dr_frq = tf.div(
                        tf.convert_to_tensor([x for x in range(self.dr_sorted.shape[0], 0, -1)], dtype=tf.float32, name="counts"),
                        self.dr_sorted.shape[0].value,
                        name="frequency"
                    )
                    tf.summary.histogram("dr_frq", self.dr_frq)

            with tf.name_scope("reg_norm_prediction"):
                self.avg = tf.reduce_mean(self.dr)
                self.scl = tf.Variable(np.random.rand(), dtype=tf.float32)
                tf.summary.scalar("scl", self.scl)
                pdt_nm_dst = dst.Normal(loc=self.avg, scale=self.scl)

                # Evaluate dr , return the predicate frequency 1-D tensor
                self.pdt_frq = pdt_nm_dst.cdf(self.dr_sorted)

                with tf.name_scope("loss"):
                    self.loss = tf.reduce_mean(tf.square((self.pdt_frq - self.dr_frq), name="error"), name="loss")
                    tf.summary.scalar("loss", self.loss)

                with tf.name_scope("train"):
                    self.train_step = tf.train.AdamOptimizer(0.001).minimize(self.loss)

            # 3rd layer to find out the thresholds to make benefit function most
            # done: complete this
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
                    self.dr_raw_p = pdt_nm_dst.prob(self.dr)
                    self.dr_prob = pdt_nm_dst.prob(self.dr, name="dr_prob")
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
                    self.dr_sgn = self._logistic_sgn.cdf(self.dr) * 2. - 1.
                    self.out_hg = (1 - self._logistic_cvt.cdf(self.dr_prob)) * (self.dp * self.dr_sgn
                              *100-20)\
                             # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

                with tf.name_scope("line_Layer_nm"):
                    self.out_nm = (-self._logistic_cvt.cdf(self.dr_prob)) *(self.dp * self.dr_sgn
                              *100-20)
                             # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

                with tf.name_scope("threshold_summary"):
                    self.bene = tf.reduce_sum(tf.add(self.out_hg, self.out_nm), name="Benefits")
                    self.bene_cvt_to_limited_interval = dst.Logistic(0., 5.).cdf(-self.bene)
                    self.trd_train = tf.train.AdamOptimizer(1e-6).minimize(self.bene_cvt_to_limited_interval)

            self.init = tf.global_variables_initializer()

            # CREATE MODEL STRUCTURE SEND #

