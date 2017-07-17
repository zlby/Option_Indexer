from abc import ABCMeta, abstractmethod


class CombineOptionsDataProvider(object):
    __metaclass__ = ABCMeta

    def __init__(self, code1, code2):
        self.code1 = code1
        self.code2 = code2

    @abstractmethod
    def get_option_price_list(self, code):
        pass

    @abstractmethod
    def get_option_rate_list(self, code):
        pass


class UnSupportDataFormatError(ValueError):
    pass
