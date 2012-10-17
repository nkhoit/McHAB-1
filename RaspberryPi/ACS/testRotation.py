import _transformations as tf
import numpy as np
import math

C = tf.euler_matrix(0,0,math.pi/2,'szyx')
print str(C)

