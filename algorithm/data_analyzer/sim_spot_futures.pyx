R"""Simulate the spot-futures prices function,

    F = (S + U) \dot \exp{ T(r-y) }
"""

from libc cimport math

# annual compound interest
cpdef float r = math.log(1.03)

cdef float _future_price(float spot_price, float time_lag, float convenience_yield, float storage_costs_discounted_value):
    return (spot_price + storage_costs_discounted_value) * math.exp(time_lag * (r - convenience_yield))

def future_price(s, t, y, u):
    return _future_price(s,t,y,u)

