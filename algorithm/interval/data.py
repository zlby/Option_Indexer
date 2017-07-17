from abc import ABCMeta, abstractmethod


class CombineOptionsDataProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_option_price_list(self, code):
        pass

    @abstractmethod
    def get_option_rate_list(self, code):
        pass


class UnSupportDataFormatError(ValueError):
    pass
