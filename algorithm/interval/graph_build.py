import tensorflow as tf
from functools import wraps
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
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

    def prepare(self, code1: str, code2: str, number: int):
        self.__preprocessing_data(code1, code2, number)

    def __preprocessing_data(self, code1: str, code2: str, number: int):
        self.positive_option_code = code1
        self.negative_option_code = code2
        self.sample_size = number
        self.positive_option_rate_list = self.__data(code=self.positive_option_code,
                                                     attribute="option_volatility_list",
                                                     number=self.sample_size)
        self.negative_option_rate_list = self.__data(code=self.negative_option_code,
                                                     attribute="option_volatility_list",
                                                     number=self.sample_size)
        self.positive_option_price_list = self.__data(code=self.negative_option_code,
                                                      attribute="option_price_list",
                                                      number=self.sample_size)
        self.negative_option_price_list = self.__data(code=self.negative_option_code,
                                                      attribute="option_price_list",
                                                      number=self.sample_size)
        self.isPrepared=True

    @staticmethod
    def __stationarity_test(ls):
        for rank in range(10):
            diff = np.diff(ls, rank)
            # noinspection PyUnresolvedReferences
            p_value = adfuller(diff)[1]
            if p_value <= 0.05:
                return rank, p_value, diff

    def __check_co_integration_relationship(self):
        """
        check whether two sequences are integrate sequence
                :param: positive_option_code: the first code of combined option
                        negative_option_code: the second code of combined option
                        number: the squence length
                :return: True or False
                """
        if not self.isPrepared:
            raise EnvironmentError("Object not prepared, call prepare() first!")
        rl1 = self.positive_option_rate_list
        rl2 = self.negative_option_rate_list

        if len(rl1) < self.sample_size or len(rl2) < self.sample_size:
            return False

        res1 = self.__stationarity_test(rl1)
        res2 = self.__stationarity_test(rl1)

        if res1 and res2:
            if res1[1] == res2[1]:
                _, p_value, _ = coint(rl1, rl2)   #coint 函数会自动调用所有cpu
                # print(p_value)
                return p_value < 0.05
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

    def get__spread_position_of_combined_options(self):
        """

        :param:
        :return: 
        """
        if not self.__check_co_integration_relationship():
            return None
        rl1 = self.positive_option_rate_list
        rl2 = self.negative_option_rate_list

        sample_size = self.sample_size
        with tf.name_scope('Input'):
            x = tf.constant(rl1, tf.float32, [1, sample_size])
            y = tf.constant(rl2, tf.float32, [1, sample_size])

        with tf.name_scope('x_add_ay'):
            # gamma = tf.Variable(np.random.rand())
            gamma = tf.Variable(-1.)
            x_add_ay = tf.add(tf.multiply(gamma, y), x)

        with tf.name_scope('loss'):
            loss = self.get_regular_normality(x_add_ay)

        with tf.name_scope('optimizer'):
            optimizer = tf.train.AdamOptimizer(learning_rate=0.05).minimize(1.-loss)

        config = tf.ConfigProto(device_count={"CPU": 8},  # limit to num_cpu_core CPU usage
                                inter_op_parallelism_threads=1,
                                intra_op_parallelism_threads=1,
                                log_device_placement=False)

        with tf.Session(config=config) as sess:
            sess.run(tf.global_variables_initializer())
            for _ in range(100):
                sess.run(optimizer)

            # more return @test
            return sess.run([gamma, loss])


            # res = y = gamma * x
            # loss = tf.placeholder(tf.float32, 0, "loss")
            # res_tensor = tf.subtract(tf.matmul(gamma, x), y)
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

    def find_max_benefit_intervals(self, gamma, sale_rate):

        # config = tf.ConfigProto(device_count={"CPU": 3},  # limit to num_cpu_core CPU usage
        #                         inter_op_parallelism_threads=1,
        #                         intra_op_parallelism_threads=1,
        #                         log_device_placement=False)
        # tf.InteractiveSession(config=config)

        p1 = self.positive_option_price_list
        p2 = self.negative_option_price_list
        r1 = self.positive_option_rate_list
        r2 = self.negative_option_rate_list

        dp = p1 + tf.multiply(gamma, p2)
        dr = r1 + tf.multiply(gamma, r2)

        __loc = tf.reduce_mean(dr)
        __scl = tf.sqrt(tf.reduce_mean(tf.square(dr - __loc)))
        nm_dst = dst.Normal(loc=__loc, scale=__scl)

        __max_raw = nm_dst.prob(__loc)
        __vrs0 = tf.Variable(np.random.rand())
        __vrs1 = tf.Variable(np.random.rand())
        trd_nm = __max_raw * dst.Logistic(0.,10.).cdf(__vrs0)
        trd_hg = trd_nm * dst.Logistic(0.,10.).cdf(__vrs1)

        sgns_in_nm = dst.Logistic(trd_nm, 0.05).cdf(nm_dst.prob(dr)) - 1.
        sgns_out_hg = dst.Logistic(trd_hg, 0.05).cdf(nm_dst.prob(dr))

        sign = dst.Logistic(0.,0.01).cdf
        step_bene = sale_rate * dp * (sgns_in_nm + sgns_out_hg) * sign(dr) - 1. * sale_rate * (1 + gamma * sign(gamma))

        benefits = tf.reduce_sum(step_bene) - sale_rate * (p1[-1] * gamma * p2[-1]) * tf.reduce_sum((sgns_out_hg + sgns_in_nm) * sign(dr))

        def find_interval(value, avg, scale):
            with tf.name_scope("find_interval_with_raw_value"):
                min_of_interval = avg - tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale
                max_of_interval = avg + tf.pow(-tf.log(2 * np.pi * scale ** 2 * value ** 2), 0.5) * scale

            return min_of_interval, max_of_interval
        #
        # nm_dst = get_data_normal_distribution_arguments()
        # trd_hg, trd_nm, max_raw = get_thresholds(nm_dst)
        # sgns = interval_signs(nm_dst.prob(r1 + tf.multiply(gamma, r2)), trd_hg, trd_nm)
        #
        #
        # step_bene = sale_rate * dp * sgns * sign(dr) - 1. * sale_rate * (1 + gamma * sign(gamma))
        # benefits = tf.reduce_sum(step_bene)
        loss = dst.Logistic(0., 30.).cdf(-benefits)
        train_step = tf.train.AdamOptimizer(0.01).minimize(loss)
        init = tf.global_variables_initializer()

        config = tf.ConfigProto(device_count={"CPU": 3},  # limit to num_cpu_core CPU usage
                                inter_op_parallelism_threads=1,
                                intra_op_parallelism_threads=1,
                                log_device_placement=False)

        with tf.Session(config=config) as sess:
            sess.run(init)
            for i in range(200):
                sess.run(train_step)
            values = sess.run([trd_hg, trd_nm])
            b1, b2 = find_interval(values[0], nm_dst.loc, nm_dst.scale)
            a1, a2 = find_interval(values[1], nm_dst.loc, nm_dst.scale)
            print(sess.run(tf.reduce_sum(sgns_out_hg + sgns_in_nm)))
            print(sess.run([trd_hg/__max_raw, trd_nm/__max_raw]))
            return sess.run([b1, a1, a2, b2, benefits])
