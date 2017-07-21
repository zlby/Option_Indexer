import tensorflow as tf
import numpy as np

def get_loss(cost):
    return cost**2

sess = tf.InteractiveSession()

number = tf.constant(5, tf.float32)

a = tf.Variable(np.random.rand(), dtype=tf.float32)

loss = tf.subtract(number, a)

sess.run(tf.variables_initializer([a]))

loss = get_loss(tf.cast(loss.eval(), tf.float32))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss**2)

# sess.run(tf.variables_initializer([optimizer]))
for i in range(10000):
    sess.run(optimizer)

print(loss.eval())


