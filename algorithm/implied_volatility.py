from scipy.optimize import fsolve
from scipy.stats import norm
import math

class Volatility:
    def __init__(self, c, s0, r, t, k):
        self.c = float(c)
        self.s0 = float(s0)
        self.r = float(r)
        self.t = float(t)
        self.k = float(k)

    def fun(self, x):
        self.sig = float(x[0])
        self.d1 = ((math.log(self.s0 / self.k) + (self.r + (self.sig ** 2) / 2) * self.t) / (self.sig * (self.t ** 0.5)))
        self.d2 = (self.d1 - self.sig * (self.t**0.5))
        return [
            self.c - (self.s0 * norm.cdf(self.d1) - self.k * (math.e ** (-self.r * self.t)) * norm.cdf(self.d2))
        ]

    def get_result(self):
        result = fsolve(self.fun, [1])
        res = result[0]
        return res
