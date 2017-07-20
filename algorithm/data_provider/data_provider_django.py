from algorithm.data_provider.data import AbstractDataProvider
from option.models import *


class DjangoDataProvider(AbstractDataProvider):

    def __call__(self, *args, **kwargs):
        if kwargs["code"]:
            __attr = kwargs["attribute"]
            if __attr == "option_price_list":
                return self.__get_option_price_list(kwargs["code"], kwargs["number"])
            elif __attr == "option_volatility_list":
                return self.__get_option_volatility_list(kwargs["code"], kwargs["number"])
            elif __attr == "future_price":
                return self.__get_future_price(kwargs["code"], kwargs["time"])
            elif __attr == "option_price":
                return self.__get_option_price(kwargs["code"], kwargs["time"])
            elif __attr == "option_volatility":
                return self.__get_option_rate(kwargs["code"], kwargs["time"])

    def __init__(self):
        # noinspection PyUnresolvedReferences
        self.query_set_future = FutureTreadingData.objects.all()
        # noinspection PyUnresolvedReferences
        self.query_set_option = OptionTreadingData.objects.all()

    def __get_option_price_list(self, code, number):
        __option_list = self.query_set_option.filter(option=code).order_by("-time")[:number]
        __price_list = []
        for __item in __option_list:
            __price_list.insert(0, __item.close_price)
        return __price_list

    def __get_option_volatility_list(self, code, number):
        __option_list = self.query_set_option.filter(option=code).order_by("-time")[:number]
        __rate_list = []
        for __item in __option_list:
            __rate_list.insert(0, __item.volatility)
        return __rate_list

    def __get_future_price(self, code, time):
        try:
            __future = self.query_set_future.get(future=code, time=time)
            return __future.close_price
        except:
            return None

    def __get_option_price(self, code, time):
        try:
            __option = self.query_set_option.get(option=code, time=time)
            return __option.close_price
        except:
            return None

    def __get_option_rate(self, code, time):
        try:
            __option = self.query_set_option.get(option=code, time=time)
            return __option.volatility
        except:
            return None
