import tensorflow as tf
from functools import wraps
import scipy.stats as scs
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
import pandas as pd
import tensorflow.contrib.distributions as dst


def run_graph(scope_name: str, loop: int = 500, feed_dict: dict = None, graph: tf.Graph = None):
    def deco(fn):
        @wraps(fn)
        def warp(*args, **kwargs):
            if graph is None:
                g = tf.Graph().as_default()
            else:
                g = graph.as_default()
            with tf.name_scope(scope_name):
                node_details = fn(args, kwargs)
            if feed_dict is None:
                return
            sess = tf.Session(graph=g)
            for x in range(loop):
                sess.run(fetches=node_details["train_step"],
                         feed_dict=feed_dict)
            return sess.run(fetches=node_details["target"],
                            feed_dict=feed_dict)

        return warp

    return deco


class GraphBuilder(object):
    """Helper Class to build a calculation graph.

    :Fields

    """
    from algorithm.data_provider.data import AbstractDataProvider

    def __init__(self, data_provider: AbstractDataProvider):
        """Class initialization method.

        :param data_provider: AbstractDataProvider
            collect, format and convert data.
        """

        self.__data = data_provider
        # List of frequency of  less than specific difference of volatility.
        self.__list_vol_frq = []
        # List of difference of volatility
        self.__list_vol = []
        # Sorted list of difference volatility
        self.__sorted_list_vol = []
        # Mean of list of difference of volatility
        self.mean_dif_vol = 0.
        pass

    def __preprocessing_data(self, code1: str, code2: str):
        self.__data()
        pass

    def __check_co_integration_relationship(self, positive_option_code: str, negative_option_code: str,
                                                 number: int):
        """
        check whether two sequences are integrate sequence
                :param: positive_option_code: the first code of combined option
                        negative_option_code: the second code of combined option
                        number: the squence length
                :return: True or False
                """
        positive_option_rate_list = self.__data(code=positive_option_code, attribute="option_volatility_list",
                                                number=number)
        negative_option_rate_list = self.__data(code=negative_option_code, attribute="option_volatility_list",
                                                number=number)
        # training_epoches = 1000
        #
        #
        # with tf.name_scope('Input'):
        #     xs = tf.placeholder(tf.float32)
        #     ys = tf.placeholder(tf.float32)
        #
        # with tf.name_scope("ratio"):
        #     alpha = tf.Variable(np.random.rand())
        #     beta = tf.Variable(np.random.rand())
        #
        # with tf.name_scope("white noise"):
        #     wn = np.random.normal()
        #
        # with tf.name_scope("prediction"):
        #     predict = tf.add(tf.multiply(alpha, xs), tf.multiply(beta, ys))
        #
        # with tf.name_scope("cost"):
        #     cost = predict - wn
        #
        # with tf.name_scope("optimizer"):
        #     optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
        #
        # with tf.name_scope("initializer"):
        #     init = tf.global_variables_initializer()
        #
        #
        # with tf.Session() as sess:
        #     sess.run(init)
        #
        #     for epoch in range(training_epoches):
        #         for (x, y) in zip(positive_option_rate_list, negative_option_rate_list):
        #             sess.run(optimizer, feed_dict={xs: x, ys: y})
        #
        #     print("finish")

            # print(sess.run(cost))
        # substract_list = []
        # for i in range(number):
        #     substract_list.append(positive_option_rate_list[i] - negative_option_rate_list[i])
        #
        # counter_positive = 0
        # df_list = pd.DataFrame(positive_option_rate_list, columns=['a'])
        # while True:
        #     data_list = df_list['a'].tolist()
        #     adf_test = adfuller(data_list)
        #     if adf_test[1] < 0.05:
        #         break
        #     counter_positive += 1
        #     df_list = df_list.diff()
        #
        #
        # print(counter_positive)

        volatility1 = np.array(positive_option_rate_list)
        volatility2 = np.array(negative_option_rate_list)

        diff_positive = volatility1
        diff_negative = volatility2
        co_integ = True
        counter = 0

        adf_tuple1 = adfuller(positive_option_rate_list)
        p_value1 = adf_tuple1[1]
        adf_tuple2 = adfuller(negative_option_rate_list)
        p_value2 = adf_tuple2[1]

        # print("Counter: %f" % counter)
        # print("adf1: %s, adf2: %s" % (format(p_value1, '.5e'), format(p_value2, '.5e')))


        while p_value1 > 0.05 and p_value2 > 0.05:
            counter += 1

            diff_positive = np.diff(diff_positive, 1)
            diff_negative = np.diff(diff_negative, 1)

            adf_tuple1 = adfuller(diff_positive.tolist())
            # print(diff_positive)
            p_value1 = adf_tuple1[1]
            adf_tuple2 = adfuller(diff_negative.tolist())
            # print(diff_negative)
            p_value2 = adf_tuple2[1]

            # print("Counter: %f" % counter)
            # print("adf1: %s, adf2: %s" % (format(p_value1, '.5e'), format(p_value2, '.5e')))

            if p_value1 < 0.05 < p_value2:
                co_integ = False
                break
            elif p_value1 < 0.05 < p_value2:
                co_integ = False
                break

            if counter > 10:
                break

        if co_integ:
            _, p_value, _ = coint(volatility1, volatility2)
            print(p_value)
            if p_value < 0.05:
                return True
            else:
                return False

    @staticmethod
    def get_regular_normality(data_list: tf.Tensor):

        def skew(a):
            with tf.name_scope("skew"):
                mean = tf.reduce_mean(a)
                result = tf.div(
                    tf.reduce_mean(
                        tf.pow(
                            tf.subtract(
                                a,
                                mean
                            ),
                            3.
                        )
                    ),
                    tf.pow(
                        tf.reduce_mean(
                            tf.square(
                                tf.subtract(
                                    a,
                                    mean
                                )
                            )
                        ),
                        1.5
                    )
                )
                a = result.eval()

            return result

        def kurtosis(a):
            with tf.name_scope("kurtosis"):
                mean = tf.reduce_mean(a)
                result = tf.div(
                    tf.reduce_mean(
                        tf.pow(
                            tf.subtract(
                                a,
                                mean
                            ),
                            4.
                        )
                    ),
                    tf.pow(
                        tf.reduce_mean(
                            tf.square(
                                tf.subtract(
                                    a,
                                    mean
                                )
                            )
                        ),
                        2.
                    )
                )

                a = result.eval()

            return result

        _s = skew(data_list)

        _k = kurtosis(data_list)

        _len = data_list.shape.as_list()[0]

        jb_value = tf.add(
            tf.div(
                tf.pow(_s, 2.) * _len,
                6.
            ),
            tf.div(
                tf.pow(_k - 3., 2.) * _len,
                24.
            )
        )

        p_value = - dst.Chi2(2.).cdf(jb_value) + 1.
        return p_value

    def __get__spread_position_of_combined_options(self, positive_option_code: str, negative_option_code: str,
                                                   number: int):
        """

        :param:
        :return: 
        """
        if not self.__check_co_integration_relationship(positive_option_code, negative_option_code, number):
            return None
        positive_option_rate_list = self.__data(code=positive_option_code, attribute="option_volatility_list",
                                                number=number)
        negative_option_rate_list = self.__data(code=negative_option_code, attribute="option_volatility_list",
                                                number=number)
        # training_epoches = 1000
        #
        #
        # with tf.name_scope('Input'):
        #     xs = tf.placeholder(tf.float32)
        #     ys = tf.placeholder(tf.float32)
        #
        # with tf.name_scope("ratio"):
        #     alpha = tf.Variable(np.random.rand())
        #     beta = tf.Variable(np.random.rand())
        #
        # with tf.name_scope("white noise"):
        #     wn = np.random.normal()
        #
        # with tf.name_scope("prediction"):
        #     predict = tf.add(tf.multiply(alpha, xs), tf.multiply(beta, ys))
        #
        # with tf.name_scope("cost"):
        #     cost = predict - wn
        #
        # with tf.name_scope("optimizer"):
        #     optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
        #
        # with tf.name_scope("initializer"):
        #     init = tf.global_variables_initializer()
        #
        #
        # with tf.Session() as sess:
        #     sess.run(init)
        #
        #     for epoch in range(training_epoches):
        #         for (x, y) in zip(positive_option_rate_list, negative_option_rate_list):
        #             sess.run(optimizer, feed_dict={xs: x, ys: y})
        #
        #     print("finish")

        # print(sess.run(cost))
        # substract_list = []
        # for i in range(number):
        #     substract_list.append(positive_option_rate_list[i] - negative_option_rate_list[i])
        #
        # counter_positive = 0
        # df_list = pd.DataFrame(positive_option_rate_list, columns=['a'])
        # while True:
        #     data_list = df_list['a'].tolist()
        #     adf_test = adfuller(data_list)
        #     if adf_test[1] < 0.05:
        #         break
        #     counter_positive += 1
        #     df_list = df_list.diff()
        #
        #
        # print(counter_positive)
        sample_size = number
        with tf.name_scope('Input'):
            x = tf.constant(positive_option_rate_list, tf.float32, [1, sample_size])
            y = tf.constant(negative_option_rate_list, tf.float32, [1, sample_size])

        with tf.name_scope('ratio_mul_x_sub_y'):
            ratio = tf.Variable(np.random.rand())
            ax_sub_y = tf.subtract(tf.matmul(ratio, x), y)

        with tf.name_scope('loss'):
            loss = self.get_regular_normality(ax_sub_y)

        with tf.name_scope('optimizer'):
            optimizer = tf.train.AdamOptimizer().minimize(loss)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for _ in range(200):
                sess.run(optimizer)

            return sess.run(ratio)


            # res = y = ratio * x
            # loss = tf.placeholder(tf.float32, 0, "loss")
            # res_tensor = tf.subtract(tf.matmul(ratio, x), y)
            # train_step = tf.train.AdamOptimizer(0.01).minimize(loss)
            # init = tf.global_variables_initializer()
            #
            # with tf.Session() as sess:
            #     sess.run(init)
            #     ls = 2
            #     for i in range(500):
            #         rs = sess.run([train_step,res], feed_dict={loss: ls})
            #         ls = self.get_regular_normality(rs[1])

        pass

    @staticmethod
    def __get_variance(data_list: tf.Tensor):
        data_tf_list = tf.cast(data_list, tf.float32)
        mean = tf.reduce_mean(data_tf_list)
        _sum = tf.pow(
            tf.subtract(data_tf_list,
                        mean),
            2.
        )
        return tf.reduce_mean(_sum)

    def __find_max_benefit_intervals(self, p1, p2, r1, r2, gamma, sale_rate):
        # no err threshold
        def get_data_normal_distribution_arguments():
            if not self.nm_dst:
                mean = tf.reduce_mean(r1 + gamma * r2)
                scl = tf.sqrt(self.__get_variance(r1 + gamma * r2))
                self.nm_dst = dst.Normal(loc=mean, scale=scl)
            return self.nm_dst

        def get_thresholds(_nm_dst):
            vrs = tf.Variable(np.random.rand(2))
            max_raw = _nm_dst.prob(tf.reduce_mean(r1 + gamma * r2))
            _threshold = vrs.value()
            trd_nm = _threshold[0] * max_raw
            trd_hg = _threshold[1] * trd_nm
            return trd_nm, trd_hg

        def interval_signs(ls: tf.Tensor, _trd_hg, _trd_nm):
            # TODO: unit test
            mr_nm_cvt = dst.Logistic(loc=_trd_nm, scale=0.05).cdf

            def ls_hg_cvt(_ls):
                _a = dst.Logistic(loc=_trd_hg, scale=0.05).cdf(_ls)
                return tf.subtract(_a, 1., tf.float32)

            return tf.add(ls_hg_cvt(ls), mr_nm_cvt(ls))

        def sign(_ls):
            _a = dst.Logistic(loc=0., scale=0.05).cdf(_ls)
            return 2. * _a - 1.

        def normalize_loss(_step_bene):
            return dst.Logistic(0., 30.).cdf(- tf.reduce_sum(_step_bene))

        def find_interval(value, avg, scale):
            with tf.name_scope("find_interval_with_raw_value"):
                min_of_interval = avg - tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale
                max_of_interval = avg + tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale
            return min_of_interval, max_of_interval

        nm_dst = get_data_normal_distribution_arguments()
        trd_hg, trd_nm = get_thresholds(nm_dst)
        sgns = interval_signs(r1 + gamma * r2, trd_hg, trd_nm)
        dp = p1 + gamma * p2
        dr = r1 + gamma * r2

        step_bene = sale_rate * (p1 + gamma * p2) * sgns * sign(r1 + gamma * r2) - 1. * sale_rate * (1 + gamma * sign(gamma))

        loss = normalize_loss(step_bene)
        train_step = tf.train.AdamOptimizer(0.01).minimize(loss)
        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            for i in range(500):
                sess.run(train_step)
            values = sess.run([trd_hg, trd_nm])
            return find_interval(values[0], nm_dst.loc, nm_dst.scale), find_interval(values[1], nm_dst.loc, nm_dst.scale)
