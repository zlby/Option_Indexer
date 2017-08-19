R"""Simulate the spot-futures prices function,

    F = (S + U) \dot \exp{ T(r-y) }
"""

from libc cimport math

# annual compound interest
r = math.log(1.03)

cdef float _future_price(float spot_price, float time_lag, float convenience_yield, float storage_costs_discounted_value):
    cdef float u = storage_costs_discounted_value
    cdef float y = convenience_yield
    cdef float t = time_lag
    cdef float s = spot_price
    return (s + u) * math.exp(t * (r - y))

def future_price(s, t, y, u):
    return _future_price(s,t,y,u)

