import tensorflow as tf
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
import pandas as pd


class GraphBuilder(object):
    from algorithm.data_provider.data import AbstractDataProvider

    def __init__(self, data_provider: AbstractDataProvider):
        self.__data = data_provider
        pass

    def __preprocessing_data(self):
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

    def __simulate_regular_normal_distribution_arguments(self):
        pass

    def __find_max_benefit_intervals(self):
        pass
