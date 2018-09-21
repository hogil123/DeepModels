from models.imgclfmodel import ImgClfModel
from dataset.dataset import Dataset

import tensorflow as tf
from tensorflow.contrib.layers import conv2d
from tensorflow.contrib.layers import max_pool2d
from tensorflow.contrib.layers import avg_pool2d
from tensorflow.contrib.layers import flatten
from tensorflow.contrib.layers import fully_connected

class DenseNet(ImgClfModel):
    # model_type = [121 | 169 | 201 \ 264]
    def __init__(self, model_type='121', k=32, theta=0.5):
        ImgClfModel.__init__(self, scale_to_imagenet=True, model_type=model_type)
        self.k = k
        self.theta = theta

    def create_model(self, input):
        k = self.k
        theta = self.theta

        with tf.variable_scope('initial_block'):
            prev_kernels = 2*k

            conv = tf.layers.batch_normalization(input)
            conv = tf.nn.relu(conv)
            conv = conv2d(conv, num_outputs=prev_kernels,
                          kernel_size=[7,7], stride=2, padding='SAME',
                          activation_fn=None)

            pool = max_pool2d(conv, kernel_size=[3,3], stride=2, padding='SAME')
            cur_layer = pool

        input_kernels = prev_kernels
        layers_concat = list()

        with tf.variable_scope('dense_block_1'):
            for i in range(6):
                bottlenect = tf.layers.batch_normalization(cur_layer)
                bottlenect = tf.nn.relu(bottlenect)
                bottlenect = conv2d(bottlenect, num_outputs=4*k,
                                    kernel_size=[1,1], stride=1, padding='SAME',
                                    activation_fn=None)

                cur_kernels = input_kernels + (k * i)
                conv = tf.layers.batch_normalization(bottlenect)
                conv = tf.nn.relu(conv)
                conv = conv2d(conv, num_outputs=cur_kernels,
                              kernel_size=[3,3], stride=1, padding='SAME',
                              activation_fn=None)

                if i is 5:
                    cur_layer = conv
                else:
                    layers_concat.append(conv)
                    cur_layer = tf.concat(layers_concat, 3)

            prev_kernels = cur_kernels

        with tf.variable_scope('transition_block_1'):
            prev_kernels = int(prev_kernels*theta)
            bottlenect = tf.layers.batch_normalization(cur_layer)
            bottlenect = conv2d(bottlenect, num_outputs=prev_kernels,
                                kernel_size=[1,1], stride=1, padding='SAME',
                                activation_fn=tf.nn.relu)

            pool = avg_pool2d(bottlenect, kernel_size=[2,2], stride=2, padding='SAME')
            cur_layer = pool
            input_kernels = prev_kernels

        layers_concat = list()

        with tf.variable_scope('dense_block_2'):
            for i in range(12):
                bottlenect = tf.layers.batch_normalization(cur_layer)
                bottlenect = tf.nn.relu(bottlenect)
                bottlenect = conv2d(bottlenect, num_outputs=4*k,
                                    kernel_size=[1,1], stride=1, padding='SAME',
                                    activation_fn=None)

                cur_kernels = input_kernels + (k * i)
                conv = tf.layers.batch_normalization(bottlenect)
                conv = tf.nn.relu(conv)
                conv = conv2d(conv, num_outputs=cur_kernels,
                              kernel_size=[3,3], stride=1, padding='SAME',
                              activation_fn=None)

                if i is 5:
                    cur_layer = conv
                else:
                    layers_concat.append(conv)
                    cur_layer = tf.concat(layers_concat, 3)

            prev_kernels = cur_kernels

        with tf.variable_scope('transition_block_2'):
            prev_kernels = int(prev_kernels*theta)
            bottlenect = tf.layers.batch_normalization(cur_layer)
            bottlenect = conv2d(bottlenect, num_outputs=prev_kernels,
                                kernel_size=[1,1], stride=1, padding='SAME',
                                activation_fn=tf.nn.relu)

            pool = avg_pool2d(bottlenect, kernel_size=[2,2], stride=2, padding='SAME')
            cur_layer = pool
            input_kernels = prev_kernels

        layers_concat = list()

        with tf.variable_scope('dense_block_3'):
            for i in range(24):
                bottlenect = tf.layers.batch_normalization(cur_layer)
                bottlenect = tf.nn.relu(bottlenect)
                bottlenect = conv2d(bottlenect, num_outputs=4*k,
                                    kernel_size=[1,1], stride=1, padding='SAME',
                                    activation_fn=None)

                cur_kernels = input_kernels + (k * i)
                conv = tf.layers.batch_normalization(bottlenect)
                conv = tf.nn.relu(conv)
                conv = conv2d(conv, num_outputs=cur_kernels,
                              kernel_size=[3,3], stride=1, padding='SAME',
                              activation_fn=None)

                layers_concat.append(conv)
                cur_layer = tf.concat(layers_concat, 3)
            prev_kernels = cur_kernels

        with tf.variable_scope('transition_block_3'):
            prev_kernels = int(prev_kernels*theta)
            bottlenect = tf.layers.batch_normalization(cur_layer)
            bottlenect = conv2d(bottlenect, num_outputs=prev_kernels,
                                kernel_size=[1,1], stride=1, padding='SAME',
                                activation_fn=tf.nn.relu)

            pool = avg_pool2d(bottlenect, kernel_size=[2,2], stride=2, padding='SAME')
            cur_layer = pool
            input_kernels = prev_kernels

        layers_concat = list()

        with tf.variable_scope('dense_block_4'):
            for i in range(16):
                bottlenect = tf.layers.batch_normalization(cur_layer)
                bottlenect = tf.nn.relu(bottlenect)
                bottlenect = conv2d(bottlenect, num_outputs=4*k,
                                    kernel_size=[1,1], stride=1, padding='SAME',
                                    activation_fn=None)

                cur_kernels = input_kernels + (k * i)
                conv = tf.layers.batch_normalization(bottlenect)
                conv = tf.nn.relu(conv)
                conv = conv2d(conv, num_outputs=cur_kernels,
                              kernel_size=[3,3], stride=1, padding='SAME',
                              activation_fn=None)

                if i is 5:
                    cur_layer = conv
                else:
                    layers_concat.append(conv)
                    cur_layer = tf.concat(layers_concat, 3)

        with tf.variable_scope('final'):
            pool = avg_pool2d(cur_layer, kernel_size=[7,7], stride=1, padding='SAME')
            flat = flatten(pool)
            self.out = fully_connected(flat, num_outputs=self.num_classes, activation_fn=None)

        return [self.out]
