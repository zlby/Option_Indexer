from abc import ABCMeta, abstractmethod


class AbstractDataProvider(object):
    """Abstract class for providing data"""
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """Self call method

        :param args: None
        :param kwargs:
            Available keyword arguments:
                code : str
                    the code of select option or future
                attribute : str
                    the attribute want to get
                number : int
                    some attribute may use
                time : str
                    same as number usage

        :return: anything you want
        """


class UnSupportDataFormatError(ValueError):
    pass

