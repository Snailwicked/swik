import os
from keras import backend as K
import tensorflow as tf

class tens():

    def __init__(self):
        K.set_session(self.get_session())

    def get_session(self,gpu_fraction=1.0):

        num_threads = os.environ.get('OMP_NUM_THREADS')
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)

        if num_threads:
            return tf.Session(config=tf.ConfigProto(
                gpu_options=gpu_options, intra_op_parallelism_threads=num_threads))
        else:
            return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))