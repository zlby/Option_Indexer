import tensorflow as tf
import algorithm.data as data
import tensorflow.contrib.distributions as dst
import numpy as np

# r1 = data.get_first_rate_list()
# r2 = data.get_second_rate_list()
# p1 = data.get_first_price_list()
# p2 = data.get_second_price_list()
# da_ten = tf.constant([r1, r2, p1, p2])
# # create a 4*N matrix tensor
#
# dr = tf.string_to_number(da_ten[0], tf.float32) - tf.string_to_number(da_ten[1], tf.float32)
# avg = tf.reduce_sum(dr) / dr.shape.dims[0].value
#
# thresholds = tf.Variable(tf.nn.top_k(tf.random_uniform([3], maxval=1.), 3).values[::-1], name="thresholds")
#
# dr_pre = tf.abs(dr[1:] / avg)
# dr_nxt = tf.abs(dr[:-1] / avg)
# dr_sgn = tf.sign(dr_nxt)
# dp = (tf.string_to_number(da_ten[2], tf.float32) - tf.string_to_number(da_ten[3], tf.float32))[1:]
#
# ops = tf.cast((dr_pre < thresholds.value()[1]) & (dr_nxt > thresholds.value()[1]), tf.float32) \
#       - tf.cast((dr_pre > thresholds.value()[0]) & (dr_nxt < thresholds.value()[0]), tf.float32) \
#       - tf.cast((dr_pre < thresholds.value()[2]) & (dr_nxt > thresholds.value()[2]), tf.float32)
#
# bene = dp * dr_sgn * 100. * ops - 20. * tf.abs(ops)
# cost = -tf.reduce_sum(bene) / bene.shape.dims[0].value
# # optimizer = tf.train.AdamOptimizer(0.1).minimize(cost)
#
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#     # for i in range(0, 1000):
#     #     sess.run(optimizer)
#     import matplotlib.pyplot as plt
#     y = sess.run(ops)
#     x = [i for i,e in enumerate(y)]
#     plt.plot(x, y)
#     plt.show()
fi = data.get_first_rate_list()
se = data.get_second_rate_list()

input = tf.placeholder(tf.float32, shape=[2, len(fi)])

dr = tf.subtract(input[0], input[1])

dr_sorted = tf.cast(tf.nn.top_k(dr, len(fi)).values, tf.float32)

temp = dr_sorted.shape[0].value

dr_frq = tf.div(
                tf.convert_to_tensor([x for x in range(dr_sorted.shape[0], 0, -1)], dtype=tf.float32, name="counts"),
                temp,
            )

avg = tf.reduce_mean(dr)
scl = tf.Variable(np.random.rand(), dtype=tf.float32)
pdt_nm_dst = dst.Normal(loc=avg, scale=scl)

pdt_frq = pdt_nm_dst.cdf(dr_sorted)



init = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init)
    print(sess.run(pdt_nm_dst, feed_dict={input: [fi, se]}))