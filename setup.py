from distutils.core import setup

from Cython.Build import cythonize

import os
targets = ["algorithm/prediction/data_analyzer/calculate_hedge_cost.pyx",
           "algorithm/prediction/data_analyzer/sim_spot_futures.pyx"]
setup(
    name='Option_Indexer',
    version='',
    packages=['test', 'test.cython', 'test.algorithm', 'client', 'client.migrations', 'option', 'option.migrations',
              'message', 'algorithm', 'algorithm.prediction', 'algorithm.prediction.data_analyzer', 'data_importer',
              'optionindexer'],
    url='',
    license='',
    author='Alan',
    author_email='',
    description='',
    ext_modules=cythonize(["algorithm/prediction/data_analyzer/calculate_hedge_cost.pyx",
                           "algorithm/prediction/data_analyzer/sim_spot_futures.pyx"])
)