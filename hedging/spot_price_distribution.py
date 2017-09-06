# from option.models import *
# import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as pl

#正态分布：
def show_normal_distribution(mean, sigma):
    x = np.arange(mean - 3 * sigma, mean + 3 * sigma, 0.01 * sigma)
    y = stats.norm.pdf(x, mean, sigma)
    result = []
    for a in zip(x, y):
        result.append(a)

    return result

    # pl.plot(x, y)
    # pl.show()

def show_triangle_distribution(a, c, b):
    # 下限为a， 众数为c， 上限为b
    loc = a
    scale = b - a
    sigma = (c - a) / scale
    x = np.arange(a, b, 0.01 * (b - a))
    y = stats.triang.pdf(x, sigma, loc, scale)

    result = []
    for a in zip(x, y):
        result.append(a)

    # pl.plot(x, y)
    # pl.show()


def show_uniform_distribution(u1, u2):
    x = np.arange(u1, u2, 0.01)
    y = stats.uniform.pdf(x, u1, u2)

    # pl.plot(x, y)
    # pl.show()

    result = []
    for a in zip(x, y):
        result.append(a)

# print(show_normal_distribution(0, 1))