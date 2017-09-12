from distutils.core import setup

from Cython.Build import cythonize

<<<<<<< HEAD
setup(
    name='Option_Indexer',
    version='',
    packages=['test', 'test.cython1', 'test.algorithm', 'client', 'client.migrations', 'option', 'option.migrations',
=======
import os
targets = ["algorithm/prediction/data_analyzer/calculate_hedge_cost.pyx",
           "algorithm/prediction/data_analyzer/sim_spot_futures.pyx"]
setup(
    name='Option_Indexer',
    version='',
    packages=['test', 'test.cython', 'test.algorithm', 'client', 'client.migrations', 'option', 'option.migrations',
>>>>>>> a8b8f2e1c441519f6dfca5902eacc0d62dc5c2cc
              'message', 'algorithm', 'algorithm.prediction', 'algorithm.prediction.data_analyzer', 'data_importer',
              'optionindexer'],
    url='',
    license='',
<<<<<<< HEAD
    author='Alan',
    author_email='',
    description='',
    ext_modules=cythonize(["algorithm/prediction/data_analyzer/calculate_hedge_cost.pyx",
                           "algorithm/prediction/data_analyzer/sim_spot_futures.pyx"])
)
=======
    author='zlby9',
    author_email='',
    description='',
    ext_modules=cythonize(targets)
)
>>>>>>> a8b8f2e1c441519f6dfca5902eacc0d62dc5c2cc
