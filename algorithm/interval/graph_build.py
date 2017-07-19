import tensorflow as tf
from functools import wraps
import numpy as np
import tensorflow.contrib.distributions as dst


def run_graph(scope_name: str, loop: int = 500, feed_dict:dict=None, graph: tf.ops.Graph = None):
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

    def __check_co_integration_relationship(self):
        pass

    def __get__spread_position_of_combined_options(self):
        pass

    @run_graph("simulate regular")
    def __simulate_regular_normal_distribution_arguments(self):
        self.scale = tf.Variable(initial_value=np.random.rand())
        # The regression regular normal distribution
        dst_nm = dst.Normal(loc=self.mean_dif_vol, scale=self.scale)
        pdt_prb_dv = dst_nm.cdf(self.__sorted_list_vol,
                                name="predict probability less than specific difference volatility")

        loss = tf.reduce_mean((pdt_prb_dv - self.__list_vol_frq) ** 2, name="regression loss")

        return {"train_step": tf.train.AdamOptimizer(0.001).minimize(loss),
                "target": self.scale}

    def __find_max_benefit_intervals(self):
        pass
