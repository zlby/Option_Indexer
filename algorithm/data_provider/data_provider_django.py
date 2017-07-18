from algorithm.data_provider.data_provider import DataProvider
from option.models import *


class DataProviderFromDjango(DataProvider):
    def __init__(self):
        self.query_set_future = FutureTreadingData.objects.all()
        self.query_set_option = OptionTreadingData.objects.all()

    def get_option_price_list(self, code, number):
        __option_list = self.query_set_option.filter(option=code).order_by("-time")[:number]
        __price_list = []
        for __item in __option_list:
            __price_list.insert(0, __item.close_price)
        return __price_list

    def get_option_rate_list(self, code, number):
        __option_list = self.query_set_option.filter(option=code).order_by("-time")[:number]
        __rate_list = []
        for __item in __option_list:
            __rate_list.insert(0, __item.volatility)
        return __rate_list

    def get_future_price(self, code, time):
        try:
            __future = self.query_set_future.get(future=code, time=time)
            return __future.close_price
        except:
            return None

    def get_option_price(self, code, time):
        try:
            __option = self.query_set_option.get(option=code, time=time)
            return __option.close_price
        except:
            return None

    def get_option_rate(self, code, time):
        try:
            __option = self.query_set_option.get(option=code, time=time)
            return __option.volatility
        except:
            return None
