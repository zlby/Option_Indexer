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

if __name__ == '__main__':

    optioncomb = CsvDataProvider("m1709c2500", "m1709c2600")

    cb = GraphBuilder(optioncomb)

    print(cb.get__spread_position_of_combined_options("m1709c2500", "m1709c2600", 10000))

# print(os.listdir("."))
#
#
# print()