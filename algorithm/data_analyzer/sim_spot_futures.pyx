R"""Simulate the spot-futures prices function,

    F = (S + U) \dot \exp{ T(r-y) }
"""

cdef extern from "math.h":
    double log(double theda)
    double exp(double theda)

import tensorflow as tf

# annual compound interest
r = log(1.03)

cdef float _future_price(float spot_price, float time_lag, float convenience_yield, float storage_costs_discounted_value):
    cdef float u = storage_costs_discounted_value
    cdef float y = convenience_yield
    cdef float t = time_lag
    cdef float s = spot_price
    return (s + u) * exp(t * (r - y))

def future_price(s, t, y, u):
    return _future_price(s,t,y,u)

def regress(spot_list, future_list, t):
    """\ln{F} = \ln{S+U} + T * (r - y)"""
    ln_f = tf.log(future_list, name="ln(F)")

    u = tf.Variable(0.,name="discounted value")
    y = tf.Variable(0.,name="convenience yield")
    ln_s_p_u = tf.log(
        tf.add(
            x=spot_list,
            y=u,
            name="foo 0"
        ),
        name="ln(U+S)"
    )

    prd = ln_s_p_u + tf.subtract(r - y) * t
    loss = tf.losses.mean_squared_error(ln_f, prd)
    train_step = tf.train.AdamOptimizer(0.01).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(500):
            sess.run(train_step)
        return sess.run([u, y])