import csv
from algorithm.data_provider.data import AbstractDataProvider
from algorithm.interval.graph_build import GraphBuilder


# import os


class CsvDataProvider(AbstractDataProvider):
    def __init__(self, code1, code2):
        import os
        root = os.path.split(os.path.realpath(__file__))[0] + "\\"
        del os
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
            ls = [float(x["vol"]) for x in self.option_datas[kwargs["code"]]]
            return ls if "number" not in kwargs else ls[-kwargs["number"]:]
        elif kwargs["attribute"] == "option_price_list":
            ls = [float(x["close"]) for x in self.option_datas[kwargs["code"]]]
            return ls if "number" not in kwargs else ls[-kwargs["number"]:]

    @staticmethod
    def getInstance():
        return CsvDataProvider(code1="m1709-c-2500", code2="m1709-c-2600")

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
              cb.get_regular_normality(tf.constant(dr[b:b + 2000], tf.float32)).eval())


def __get_ratio_test():
    optioncomb = CsvDataProvider("m1709c2500", "m1709c2600")
    cb = GraphBuilder(optioncomb)
    r1 = optioncomb(attribute="option_volatility_list", code="m1709c2500")
    r2 = optioncomb(attribute="option_volatility_list", code="m1709c2600")
    cb.prepare(code1='m1709c2500', code2='m1709c2600', number=2000)
    ratio = cb.get__spread_position_of_combined_options()
    print(ratio)


def __get_interval_test():
    dataprovider = CsvDataProvider("m1709-c-2500", "m1709-c-2600")
    cb = GraphBuilder(dataprovider)
    cb.prepare(code1='m1709-c-2500', code2='m1709-c-2600', number=2000)
    ratio = cb.get__spread_position_of_combined_options()
    print(ratio)
    res = cb.find_max_benefit_intervals(ratio[0], 10.)
    print(res)


if __name__ == "__main__":
    # __get_regular_normality_test()
    __get_interval_test()
