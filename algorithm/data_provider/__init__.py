r"""Data providers

Abstract Class:

    AbstractDataProvider:

        Author:

            Alan WANG (alan1995wang@outlook.com)

        Method:

            __init__(self)

Class:

    DjangoDataProvider:

        Author:
            周梁博雅 (Null)

        Method:

            __call__(self, *args, **kwargs)__

"""
from algorithm.data_provider.data import *
try:
    from algorithm.data_provider.data_provider_django import *
except:
    pass