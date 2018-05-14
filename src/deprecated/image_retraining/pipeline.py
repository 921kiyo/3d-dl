# Disable "The TensorFlow library wasn't compiled to use SSE instructions"
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# import tensorflow as tf

# # constant = tf.constant("hello")

# # Non constant data
# x = tf.placeholder(tf.string)

# # Evaluating nodes
# with tf.Session() as sess:
#     output = sess.run(x, feed_dict= {x: 'Hello World'})
    # print(output)

# Solution is available in the other "solution.py" tab
import tensorflow as tf

# # TODO: Convert the following to TensorFlow:
# x = tf.constant(10)
# y = tf.constant(2)
# z = tf.subtract(tf.divide(x,y),tf.cast(tf.constant(1), tf.float64))

# with tf.Session() as sess:
#     output = sess.run(z)
#     print(output)

tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)