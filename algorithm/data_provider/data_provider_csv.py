import csv
from algorithm.data_provider.data_provider import DataProvider


class DataProviderFromCSV(DataProvider):
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

    def get_option_price_list(self):
        return ([float(x["close"]) for x in self.option_datas[str(self.code1)]],
                [float(x["close"]) for x in self.option_datas[str(self.code2)]])

    def get_option_rate_list(self, code):
        return ([float(x["vol"]) for x in self.option_datas[str(self.code1)]],
                [float(x["vol"]) for x in self.option_datas[str(self.code2)]])

    def get_future_price(self, code, time):
        pass

    def get_option_price(self, code, time):
        pass

    def get_option_rate(self, code, time):
        pass
