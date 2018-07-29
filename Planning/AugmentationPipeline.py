import time
import tensorflow as tf
from six.moves import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import skimage.transform as skt
import skimage.io as io
from skimage import exposure, img_as_float, img_as_uint
import os

"""
References and code snippets from:
Tensorflow manual: https://www.tensorflow.org/api_guides/python/reading_data
FIFOqueu usage: https://blog.metaflow.fr/tensorflow-how-to-optimise-your-input-pipeline-with-queues-and-multi-threading-e7c3874157e0
TFRecords binary format guide: http://warmspringwinds.github.io/tensorflow/tf-slim/2016/12/21/tfrecords-guide/
Data Feeding: https://indico.io/blog/tensorflow-data-inputs-part1-placeholders-protobufs-queues/
"""

tfrecords_filename = 'D:\\PycharmProjects\\OcadoPlanning\\5010171005204.tfrecords'
product_file = 'D:\\PycharmProjects\\product-image-dataset-v0.1\\5010171005204_2017-11-30_17.20.19\\5010171005204'
IMAGE_WIDTH =1280
IMAGE_HEIGHT =1024
IMAGE_DEPTH = 3

class ImageReader(object):
    def __init__(self, filenames, num_epochs=1, queue_cap=50, num_threads=1):
        self.filename_q = self.create_file_label_queue(filenames, num_epochs)
        _image, _label = self.read_and_augment_single()
        #initialize the variables
        self.init_op = tf.group(tf.global_variables_initializer(),
                                tf.local_variables_initializer())

        # sample queue definitions
        self.sample_q = tf.FIFOQueue(capacity=queue_cap, dtypes=[tf.float64, tf.int64])
        _enqueue_op = self.sample_q.enqueue([_image, _label])
        _numberOfThreads = num_threads # more to reduce the probability CPU is idle!
        self.sample_qrunner = tf.train.QueueRunner(self.sample_q, [_enqueue_op] * _numberOfThreads)
        tf.train.add_queue_runner(self.sample_qrunner)
        self.input_pair = self.sample_q.dequeue() # fetch input pair [image,label]
        self.input_image = self.input_pair[0]
        self.input_label = self.input_pair[1]

    def create_file_label_queue(self, filenames, num_epochs):
        raise NotImplementedError

    def read_and_decode_single(self):
        raise NotImplementedError

    @staticmethod
    def adaptive_equalize(img):
        # Adaptive Equalization
        img = img_as_float(img)
        img_adapteq = exposure.equalize_hist(img)
        return img_adapteq

    @staticmethod
    def tf_equalize(self, img_tnsr):
        image_rot = tf.py_func(adaptive_equalize, [img_tnsr], tf.float64)
        image_rot.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH])  # when using pyfunc, need to do this??
        return image_rot

    def read_and_augment_single(self):
        _image, _label = self.read_and_decode_single()
        _image = tf.cast(_image, tf.float64)
        _image = tf.image.random_flip_left_right(_image)
        '''
        # This is too expensive!
        angle = tf.random_uniform(shape=(1,), minval=-45. * np.pi / 180., maxval=45. * np.pi / 180., dtype=tf.float32)
        Image.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH])  # why do I have to always do this?
        Image = tf.contrib.image.rotate(Image, angle)
        '''
        return _image, _label

'''
This reader assumes that the examples have been parsed into a tfrecords file, with features in the format:
{height : tf.int64, width : tf.int64, image_raw : tf.string, label: tf.int64}
This can be done beforehand with the Jpg2TFRecord.py file
The reader will proceed to read from the list of TFRecords filenames, where the filenames will be randomly
shuffled
'''
class TFRecordsReader(ImageReader):

    def __init__(self, filenames, num_epochs=1, queue_cap=50, num_threads=1):
        super(TFRecordsReader, self).__init__(
            filenames, num_epochs=num_epochs, queue_cap=queue_cap, num_threads=num_threads)

    def create_file_label_queue(self, filenames, num_epochs):
        return tf.train.string_input_producer(filenames, num_epochs=num_epochs)

    def read_and_decode_single(self):
        reader = tf.TFRecordReader()

        _, serialized_example = reader.read(self.filename_q)

        features = tf.parse_single_example(
            serialized_example,
            # Defaults are not specified since both keys are required.
            features={
                'height': tf.FixedLenFeature([], tf.int64),
                'width': tf.FixedLenFeature([], tf.int64),
                'image_raw': tf.FixedLenFeature([], tf.string),
                'label': tf.FixedLenFeature([], tf.int64)
            })

        # convert image into uint8
        image_tnsr = tf.decode_raw(features['image_raw'], tf.uint8)
        _label = features['label']
        image_tnsr = tf.cast(image_tnsr, tf.uint8)

        image_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH)
        image_tnsr = tf.reshape(image_tnsr, image_shape)
        return image_tnsr, _label


'''
This reader assumes that the jpeg examples are placed in folders of format <root>/**/<label>/sample.jpg
for every folder given to JpegReader, it will recursively walk the dir tree, with the assumption that
the immediate containing folder of every jpeg file being the label.
'''
class JpegReader(ImageReader):

    def __init__(self, filenames, num_epochs=1, queue_cap=50, num_threads=1):
        super(JpegReader, self).__init__(
            filenames, num_epochs=num_epochs, queue_cap=queue_cap, num_threads=num_threads)

    '''num_epochs currently has no effect on this method, TODO: sort this out!'''
    def create_file_label_queue(self, filenames, num_epochs):
        files = []
        labels = []

        for folder in filenames:
            for (dirpath, dirnames, _files) in os.walk(folder):
                for filename in _files:
                    files.append(os.path.join(dirpath, filename))
                    labels.append(np.int64(os.path.basename(dirpath)))

        files_tensor = tf.constant(files)
        labels_tensor = tf.constant(labels)

        print('We have this many files: ' + str(len(files)))

        # create the queue
        file_label_q = tf.RandomShuffleQueue(len(files), 0, [tf.string, tf.int64], shapes=[[], []])
        # all the admin
        _enqueue_op = file_label_q.enqueue_many([files_tensor, labels_tensor])
        qr = tf.train.QueueRunner(file_label_q, [_enqueue_op] )
        tf.train.add_queue_runner(qr)

        return file_label_q

    def read_and_decode_single(self):

        image_filename, image_label = self.filename_q.dequeue()
        image_file = tf.read_file(image_filename)

        image_tnsr = tf.image.decode_jpeg(image_file) # decodes into uint8 tensor

        image_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH)
        image_tnsr = tf.reshape(image_tnsr, image_shape)
        return image_tnsr, image_label


im_read = TFRecordsReader([tfrecords_filename], num_threads=3)
#im_read = JpegReader([product_file], num_threads=3)

with tf.Session() as sess:
    sess.run(im_read.init_op)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    time_start = time.time()
    # Let's read off 3 batches just for example
    for i in range(500):
        img, label = sess.run([im_read.input_image, im_read.input_label])

        # We selected the batch size of two
        # So we should get two image pairs in each batch
        # Let's make sure it is random
        if(not(i%50)):
            time_end = time.time()
            q_size = sess.run(im_read.sample_q.size())
            print('current queue size: ' + str(q_size))
            print('Time to enqueue 50 samples: ' + str(time_start-time_end))
            time_start = time.time()

    coord.request_stop()
    coord.join(threads)
