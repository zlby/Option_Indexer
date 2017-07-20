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

        pass

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



        pass

    @staticmethod
    def get_regular_normality(data_list: list):
        return 100 * scs.normaltest(data_list)[1]

    @staticmethod
    def __get_variance(data_list):
        data_tf_list = tf.cast(data_list, tf.float32)
        mean = tf.reduce_mean(data_tf_list)
        _sum = tf.pow(
            tf.subtract(data_tf_list,
                        mean),
            2.
        )
        return tf.reduce_mean(_sum)

    def __find_max_benefit_intervals(self):
        pass
