from __future__ import absolute_import
import tensorflow as tf
from .sim_spot_futures import r
def regress(spot_list, future_list, t):
    """\ln{F} = \ln{S+U} + T * (r - y)"""
    ln_f = tf.log(future_list, name="l")

    u = tf.Variable(0.,name="discountedvalue")
    y = tf.Variable(0.,name="convenienceyield")
    ln_s_p_u = tf.log(
        tf.add(
            x=spot_list,
            y=u,
            name="foo0"
        ),
        name="ln"
    )

    prd = ln_s_p_u + tf.subtract(r, y) * t
    loss = tf.losses.mean_squared_error(ln_f, prd)
    train_step = tf.train.AdamOptimizer(0.01).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(500):
            sess.run(train_step)
        return sess.run([u, y])
