from option.models import *
import datetime
import numpy as np
import scipy.stats as stats
from algorithm.prediction.lstmcore import *

#正态分布：
def show_normal_distribution(mean, sigma):
    mean = float(mean)
    sigma = float(sigma)
    x = np.arange(mean - 3 * sigma, mean + 3 * sigma, 0.06 * sigma)
    y = stats.norm.pdf(x, mean, sigma)
    result = []
    for a in zip(x, y):
        result.append(a)

    return result

    # pl.plot(x, y)
    # pl.show()

def show_triangle_distribution(a, c, b):
    # 下限为a， 众数为c， 上限为b
    a = float(a)
    c = float(c)
    b = float(b)
    loc = a
    scale = b - a
    sigma = (c - a) / scale
    x = np.arange(a, b, 0.02 * (b - a))
    y = stats.triang.pdf(x, sigma, loc, scale)

    result = []
    for a in zip(x, y):
        result.append(a)

    # pl.plot(x, y)
    # pl.show()

    return result


def show_uniform_distribution(u1, u2):
    u1 = float(u1)
    u2 = float(u2)
    x = np.arange(u1, u2, 0.02 * abs(u2 - u1))
    y = stats.uniform.pdf(x, u1, u2)

    # pl.plot(x, y)
    # pl.show()

    result = []
    for a in zip(x, y):
        result.append(a)

    return result

lstm = None

def get_predict(time_future:datetime.datetime):
    global lstm
    query_spot = Spot.objects.all().order_by('-time')[:200]
    spot_list = []
    for item in query_spot:
        spot_list.insert(0, item.price)

    spot_list = np.asarray(spot_list)
    today = datetime.date.today()
    future_day = datetime.date(year=time_future.year, month=time_future.month, day=time_future.day)
    day_length = (future_day - today).days
    if not lstm:
        lstm = LstmModel(spot_list)
    u = lstm.predict(day_length)[-1]

    return u


def show_predict(time_future:datetime.datetime):
    return show_normal_distribution(get_predict(time_future), 1)