import time
import tensorflow as tf
from six.moves import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import skimage.transform as skt
import skimage.io as io
import os
import imageio

root_folder = 'D:\\PycharmProjects\\product-image-dataset-v0.1' \
         '\\5010171005204_2017-11-30_17.20.19'
label = 5010171005204
folder = os.path.join(root_folder, str(label))
IMAGE_WIDTH =1280
IMAGE_HEIGHT =1024
IMAGE_DEPTH = 3

image_files = []
for (dirpath, dirnames, filenames) in os.walk(folder):
    image_files.extend(filenames)
    break

image_data = np.ndarray(shape=(len(image_files), IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH),
                         dtype=np.uint8)
n_image_read = 0
for file in image_files:
    image_file = os.path.join(folder, file)
    image_data[n_image_read,:,:,:] = imageio.imread(image_file)
    n_image_read += 1

print('Loaded all images into memory')

tfrecords_filename = str(label) + '.tfrecords'

'''writing into TFRecords format'''

writer = tf.python_io.TFRecordWriter(tfrecords_filename)

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

for n in range(n_image_read):
    img = image_data[n]

    img_raw = img.tostring()  # label already in string format
    label_raw = np.int64(label)

    # tf.train.Example is the default format for storing in TFRecords
    # construct the Example proto object
    example = tf.train.Example(features=tf.train.Features(feature={
        'height': _int64_feature(IMAGE_WIDTH),
        'width': _int64_feature(IMAGE_HEIGHT),
        'image_raw': _bytes_feature(img_raw),
        'label': _int64_feature(label_raw)}))

    writer.write(example.SerializeToString())

writer.close()

"""
'''assessing TF record format'''
record_iterator = tf.python_io.tf_record_iterator(path=tfrecords_filename)
n = 0
num_diff = 0
for string_record in record_iterator:

    example = tf.train.Example()
    example.ParseFromString(string_record)

    img_string = (example.features.feature['image_raw']
                  .bytes_list
                  .value[0])

    reconstructed_label = int(example.features.feature['label']
                         .int64_list
                         .value[0])

    img_1d = np.fromstring(img_string, dtype=np.uint8)
    reconstructed_img = img_1d.reshape((IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH))

    original_img = image_data[n]
    original_label = label
    if(not(np.allclose(original_img, reconstructed_img)) or
           not(np.allclose(original_label, reconstructed_label))):
        num_diff += 1
    n += 1

print('Number of mismatches: ' + str(num_diff))
"""