from abc import ABCMeta, abstractmethod


class DataProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_option_price_list(self, code):
        pass

    @abstractmethod
    def get_option_rate_list(self, code):
        pass

    @abstractmethod
    def get_option_price(self, code, time):
        pass

    @abstractmethod
    def get_future_price(self, code, time):
        pass

    @abstractmethod
    def get_option_rate(self, code, time):
        pass


class UnSupportDataFormatError(ValueError):
    pass




