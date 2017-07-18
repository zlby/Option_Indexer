from algorithm.data_provider.data_provider_django import DjangoDataProvider


class GraphBuilder(object):
    from algorithm.data_provider.data import AbstractDataProvider

    def __init__(self, data_provider: AbstractDataProvider):
        self.__data = data_provider
        pass

    def __check_co_integration_relationship(self):
        dp = DjangoDataProvider()
