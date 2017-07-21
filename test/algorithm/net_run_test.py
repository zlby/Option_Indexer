import csv
import algorithm.interval.net_run as net
from algorithm.data_provider.data import *
from algorithm.interval.graph_build import GraphBuilder


# import os


class CsvDataProvider(AbstractDataProvider):

    def __init__(self, code1, code2):
        root = "./"

        self.option_codes = (str(code1), str(code2))
        self.option_datas = {}
        with open(root + str(code1) + ".csv") as f_1:
            data_1 = csv.DictReader(f_1, delimiter=";")
            self.option_datas[str(code1)] = [x for x in data_1]
        with open(root + str(code2) + ".csv") as f_2:
            data_2 = csv.DictReader(f_2, delimiter=";")
            self.option_datas[str(code2)] = [x for x in data_2]

    def __call__(self, *args, **kwargs):
        if kwargs["attribute"] == "option_volatility_list":
            return [float(x["vol"]) for x in self.option_datas[kwargs["code"]]]
        elif kwargs["attribute"] == "option_price_list":
            return [float(x["close"]) for x in self.option_datas[kwargs["code"]]]


def __get_regular_normality_test():

    optioncomb = CsvDataProvider("m1709c2500", "m1709c2600")

    cb = GraphBuilder(optioncomb)

    r1 = optioncomb(attribute="option_volatility_list", code="m1709c2500")
    r2 = optioncomb(attribute="option_volatility_list", code="m1709c2600")
    import numpy as np
    dr = np.subtract(r2, r1)
    dr = np.subtract(dr[1:], dr[:-1])

    import tensorflow as tf

    tf.InteractiveSession()
    for i in range(10):
        a = tf.random_normal([2000])
        b = np.random.randint(6000)
        print(cb.get_regular_normality(a).eval(),
         cb.get_regular_normality(tf.constant(dr[b:b+2000], tf.float32)).eval())

    # if (cb.get_regular_normality(dr) < 0.1) &\
    #     (cb.get_regular_normality(a_list) > 50 )&\
    #     (cb.get_regular_normality(b_list) < 0.05):
    #     print("__get_regular_normality_test passed")

if __name__ == "__main__":
    __get_regular_normality_test()
