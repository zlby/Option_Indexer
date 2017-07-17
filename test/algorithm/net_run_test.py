from algorithm.interval.data import *
import algorithm.interval.net_run as net
import csv
import os

from algorithm.interval.net_graph_build import SubGraph


class CsvDataProvider(CombineOptionsDataProvider):

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

    def get_option_rate_list(self, code):
        if code not in self.option_codes:
            raise ValueError
        else:
            return [float(x["vol"]) for x in self.option_datas[str(code)]]

    def get_option_price_list(self, code):
        if code not in self.option_codes:
            raise ValueError
        else:
            return [float(x["close"]) for x in self.option_datas[str(code)]]

if __name__ == '__main__':

    optioncomb = CsvDataProvider("m1709c2500", "m1709c2600")

    print(net.get_interval("m1709c2500", "m1709c2600", graph=SubGraph(), options=optioncomb))
# print(os.listdir("."))
#
#
# print()