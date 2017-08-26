import tensorflow as tf

sess = tf.InteractiveSession()

var = tf.Variable(5.)

# pla = tf.placeholder(tf.float32)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(var)


sess.run(tf.global_variables_initializer())
# print(con.eval())
print(var.eval())
# print(pla.eval())
# print(optimizer.eval())
sess.close()