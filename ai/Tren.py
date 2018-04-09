import tensorflow as tf
import numpy as np

from snek.Snake import Snek, LEFT

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

s: Snek = Snek(20, 20, 5, LEFT)

a = s.snake_coordinates()
a.append((s.food_x, s.food_y))
a.append((s.width, s.height))

tensor = tf.convert_to_tensor(a, tf.int32)

print(tensor)

sess = tf.Session()
out_z = sess.run(tensor)

print(out_z)
