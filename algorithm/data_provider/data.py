from abc import ABCMeta, abstractmethod


class AbstractDataProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class UnSupportDataFormatError(ValueError):
    pass

