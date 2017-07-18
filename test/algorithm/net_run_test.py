import csv

import algorithm.interval.net_run as net
from algorithm.data_provider.data import *
from algorithm.interval.net_graph_build import SubGraph


# import os


class CsvDataProvider(AbstractDataProvider):

    def __call__(self, *args, **kwargs):
        return [float(x[kwargs["attribute"]]) for x in self.option_datas[kwargs["code"]]]

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

if __name__ == '__main__':

    optioncomb = CsvDataProvider("m1709c2500", "m1709c2600")


    print(net.get_interval("m1709c2500", "m1709c2600", graph=SubGraph().build_graph(8640), options=optioncomb))
# print(os.listdir("."))
#
#
# print()