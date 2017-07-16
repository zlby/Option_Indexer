# import data
import algorithm.database_link as dl
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


with tf.Graph().as_default() as g:
    with tf.name_scope('Input'):
        inputs = tf.placeholder(tf.float32, shape=[4, 2000], name='inputs')
        # nm_args = tf.Variable(tf.zeros([2], tf.float32, name="normal arguments"))
        dr = tf.subtract(inputs[1], inputs[0], name="dr")
        # former_dr = ([0]+dr)[0:sample_size]  # TODO change

        dp = tf.subtract(inputs[3], inputs[2], name="dp")
        with tf.name_scope('frequency'):
            dr_sorted = tf.cast(tf.nn.top_k(dr, 2000).values, tf.float32, name="dr_sorted")
            dr_frq = tf.div(
                tf.convert_to_tensor([x for x in range(dr_sorted.shape[0], 0, -1)], dtype=tf.float32, name="counts"),
                dr_sorted.shape[0].value,
                name="frequency"
            )
            tf.summary.histogram("dr_frq", dr_frq)

    with tf.name_scope("reg_norm_prediction"):
        avg = tf.reduce_mean(dr)
        scl = tf.Variable(np.random.rand(), dtype=tf.float32)
        tf.summary.scalar("scl", scl)
        pdt_nm_dst = dst.Normal(loc=avg, scale=scl)

        # Evaluate dr , return the predicate frequency 1-D tensor
        pdt_frq = pdt_nm_dst.cdf(dr_sorted)

        with tf.name_scope("loss"):
            loss = tf.reduce_mean(tf.square((pdt_frq - dr_frq), name="error"), name="loss")
            tf.summary.scalar("loss", loss)

        with tf.name_scope("train"):
            train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

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
            _thresholds = tf.Variable(np.random.rand(3), dtype=tf.float32, name="_thresholds")
            tf.summary.histogram("tsd_var", _thresholds)
            # Fixed: want to return the value of the PDFunction when key equals avg, maybe wrong?

            max_raw_p = pdt_nm_dst.prob(avg)
            dr_raw_p = pdt_nm_dst.prob(dr)
            dr_prob = pdt_nm_dst.prob(dr, name="dr_prob")
            # former_dr_prob = pdt_nm_dst.prob(former_dr)

            # Get _thresholds latest snapshot values
            _thresholds_values = dst.Logistic(0., 3.).cdf(_thresholds.value())
            trd_nm = max_raw_p * _thresholds_values[0]
            trd_hg = trd_nm * _thresholds_values[1]
            trd_err = trd_hg * _thresholds_values[2]

            # solved : correctly get its value?
            interval_nm = find_interval(trd_nm, avg, scl.value())
            interval_hg = find_interval(trd_hg, avg, scl.value())
            interval_err = find_interval(trd_err, avg, scl.value())

        _logistic_cvt = dst.Logistic(loc=trd_hg, scale=0.1)
        _logistic_sgn = dst.Logistic(loc=0., scale=0.1)
        # _logistic_diff = dst.Logistic(loc=0., scale=0.01)

        # for i in range(sample_size)[1:]:
        #     dr_change=_logistic_cvt.cdf(_logistic_cvt.cdf(dr_prob[i-1])*_logistic_cvt.cdf(dr_prob[i]))
        #     dr_sgn=

        with tf.name_scope("line_Layer_hg"):
            dr_sgn = _logistic_sgn.cdf(dr) * 2. - 1.
            out_hg = (1 - _logistic_cvt.cdf(dr_prob)) * (dp * dr_sgn
                      *100-20)\
                     # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

        with tf.name_scope("line_Layer_nm"):
            out_nm = (-_logistic_cvt.cdf(dr_prob)) *( dp * dr_sgn
                      *100-20)
                     # * _logistic_diff.cdf(tf.multiply(_logistic_cvt.cdf(former_dr_prob), _logistic_cvt.cdf(dr_prob)))

        with tf.name_scope("threshold_summary"):
            bene = tf.reduce_sum(tf.add(out_hg, out_nm), name="Benefits")
            bene_cvt_to_limited_interval = dst.Logistic(0., 5.).cdf(-bene)
            trd_train = tf.train.AdamOptimizer(1e-6).minimize(bene_cvt_to_limited_interval)

    init = tf.global_variables_initializer()

    # CREATE MODEL STRUCTURE SEND #

    saver = tf.train.Saver()
