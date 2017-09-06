import tensorflow as tf
from algorithm.prediction.data_analyzer.sim_spot_futures import r


def regress(spot_list, future_list, t):
    """\ln{F} = \ln{S+U} + T * (r - y)"""
    ln_f = tf.log(future_list, name="ln(F)")

    u = tf.Variable(0., name="discounted value")
    y = tf.Variable(0., name="convenience yield")
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