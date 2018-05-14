#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from datetime import datetime
import hashlib
import os.path
import random
import re
import sys
import tarfile
import numpy as np
import tensorflow as tf

from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile
from sklearn.manifold import TSNE

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from skimage import exposure, img_as_float, img_as_ubyte
import json
import re
import itertools
from sklearn.metrics import confusion_matrix
import matplotlib
import io
import pickle
from kerasmodels.keras_eval_errors import *

from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras import optimizers
from time import *
import os
from keras.models import load_model

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

class KerasEval:
    def __init__(self):
        pass

    def create_label_lists(self, label_path):
        """
        creates a label to encoding dict and a reverse dict via an output
        label txt file generated by retraining.py
        :param label_path: output label file name
        :param json_path: path to product json file
        :return: label to encoding dict and a reverse of that
        """
        with open(label_path) as f:
            labels = f.readlines()
        labels = [l.strip() for l in labels]

        label2idx = {}
        idx2label = {}
        for label_idx, label_name in enumerate(labels):
            label2idx[label_name] = label_idx
            idx2label[label_idx] = label_name

        return label2idx, idx2label

    def get_test_files(self, filedir, label2idx, n=5):
        """
        Iterates through the folder structure and picks a random file from
        each folder. Goes through folder structure n times
        :param filedir: directory containing the folders/files
        :param label2idx: dict containing the encoding of each label
        :param n: number of times to iterate over folder structure
        :return: list of tuples of the form (label, encoding, filepath)
        """

        test_files = [] #list of (label, filename) tuple
        count_labels = 0

        for (dirpath, dirnames, filenames) in os.walk(filedir):
            if dirpath == filedir:
                continue
            num_files = len(filenames)
            if num_files > n:
                num_files = n

            # Extract the last dir name from dirpath
            last_dirname = os.path.basename(os.path.normpath(dirpath))
            if(last_dirname in label2idx.keys()):
                new_dir = os.path.join(filedir, last_dirname)
                # Check if the directory has only one level below and not more than that
                if(dirpath != new_dir):
                    raise InvalidDirectoryStructureError()

                for i in range(num_files):
                    if not (filenames[i].endswith('.jpg')):
                        continue
                    filepath = os.path.join(dirpath,filenames[i])
                    label = os.path.basename(dirpath)
                    test_files.append((label, label2idx[label], filepath))

        return test_files

    def eval_result(self, result_tensor, ground_truth, idx2label):
        """
        Run prediction and compare the results with the correct labels
        :param result_tensor: prediction model
        :param ground_truth: dict containing the correct labels
        :param idx2label: dict containing the labels of each encoding
        :return: prediction result, correct label, predicted label and max score
        """
        if not check_confidence_tensor(result_tensor):
            raise InvalidInputError('Result confidence tensor invalid!')

        result = np.argmax(result_tensor,axis=1)
        prediction = (ground_truth==result[0])
        correct_label = idx2label[ground_truth]
        predicted_label = idx2label[result[0]]
        max_score = np.amax(result_tensor,axis=1)
        print("predicted: ", predicted_label, "correct: ", correct_label)
        return prediction, correct_label, predicted_label, max_score

    def extract_summary_tensors(self, test_results, label2idx):
        """
        Get evaluation components we will export to Tensorboard
        :param test_results: result of the prediction per class
        :param label2idx: dict containing the encoding of each label
        :return: np array of confidences, predictions and correct labels
        """
        confidences = []
        predictions = []
        truth = []

        for result in test_results:
            confidences.extend(result['class_confidences'])# of shape [batch_size, n_class]
            predictions.append(label2idx[result['predicted_label']])
            truth.append(label2idx[result['correct_label']])

        confidences = np.array(confidences)
        predictions = np.array(predictions)
        truth = np.array(truth)
        return confidences, predictions, truth

    def plot_confusion_matrix(self, cm, classes, normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        :param cm: Confusion Matrix plot
        :param classes: list for classes with labels and encoding of each label
        :param normalize: Boolean for applying normalisation
        :param title: Title of the plot
        :param cmap: color map for plot
        :return: tensor image to be exported to Tensorboard
        """
        if (not check_confusion_matrix(cm)):
            raise InvalidInputError('Confusion Matrix Invalid!')
        if not (len(classes) == cm.shape[0]):
            raise InvalidInputError('Number of classes incompatible with CM!')
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

        # convert to tf image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = tf.image.decode_png(buf.getvalue(), channels=4)
        image = tf.expand_dims(image, 0)
        plt.clf()

        return image

    def compute_sensitivity(self, cm):
        """
        Calculate the sensitivity of the classification performance and that of average
        :param cm: Confusion Matrix plot
        :return: np array of sensitivity and mean sensitivity
        """
        if (not check_confusion_matrix(cm)):
            raise InvalidInputError('Confusion Matrix Invalid!')

        cm = np.array(cm)
        relevant = np.sum(cm,axis=1)
        sensitivity = np.zeros(relevant.shape)
        for i in range(len(sensitivity)):
            if relevant[i] == 0:
                sensitivity[i] = -1
                continue
            sensitivity[i] = cm[i,i]/relevant[i]
        average_sensitivity = np.mean(sensitivity)
        return sensitivity, average_sensitivity

    def compute_precision(self, cm):
        """
        Calculate the precision of the classification
        :param cm: Confusion Matrix plot
        :return: np array of precision and mean precision
        """
        if (not check_confusion_matrix(cm)):
            raise InvalidInputError('Confusion Matrix Invalid!')

        cm = np.array(cm)
        relevant = np.sum(cm,axis=0)
        precision = np.zeros(relevant.shape)
        for i in range(len(precision)):
            if relevant[i] == 0:
                precision[i] = -1
                continue
            precision[i] = cm[i,i]/relevant[i]
        average_precision = np.mean(precision)
        return precision, average_precision

    def compute_accuracy(self, cm):
        """
        Calculate the accuracy of the classification
        :param cm: Confusion Matrix plot
        :return: accuray
        """
        if (not check_confusion_matrix(cm)):
            raise InvalidInputError('Confusion Matrix Invalid!')

        cm = np.array(cm)
        relevant = np.sum(np.sum(cm))
        accuracy = np.sum(np.diag(cm))/relevant
        return accuracy

    def plot_bar(self, x,heights, heights2=None, title='Bar Chart', xlabel='X', ylabel='Y'):
        """
        Drawing precision and sensitivity plot
        :param x: length of dict containing the encoding of each label
        :param heights: precision
        :param heights2: sensitivity
        :param title: title of the plot
        :param xlabel: x label for the plot
        :param ylabel: y label for the plot
        :return: tensor image to be exported to Tensorboard
        """
        bar_width = 0.4
        x = np.array(x)
        plt.bar(x,heights,bar_width)
        if heights2 is not None:
            plt.bar(x-bar_width,heights2,bar_width)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.tight_layout()

        # convert to tf image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = tf.image.decode_png(buf.getvalue(), channels=4)
        image = tf.expand_dims(image, 0)
        plt.clf()

        return image

    def summarize_results(self, sess, label2idx, per_class_test_results, model_source_dir, print_results=False):
        """
        Sending all components to Tensorboard
        :param sess: Tensorflow session
        :param label2idx: dict containing the encoding of each label
        :param per_class_test_results: dictionary containing correct and predicted labels
        :param model_source_dir: output folder
        :param print_results: boolean value to determine whether the matrices are printed or not
        :return: Dictionary containing all the matrices
        """

        # Check if directory already exists. If so, create a new one
        if tf.gfile.Exists(model_source_dir + '/test_results'):
            tf.gfile.DeleteRecursively(model_source_dir + '/test_results')
        tf.gfile.MakeDirs(model_source_dir + '/test_results')

        # create the summary setup
        summary_writer = tf.summary.FileWriter(model_source_dir + '/test_results', sess.graph)

        # Create decoding tensors
        jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
        decoded_image =tf.image.decode_jpeg(jpeg_data, channels=3)
        decoded_image_4d = tf.expand_dims(decoded_image, 0)
        resize_shape = tf.stack([150, 150])
        resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
        resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                                 resize_shape_as_int)

        predicted_placeholder = tf.placeholder(tf.string, name="PredictedLabel")
        c = len(label2idx.keys())

        predictions = []
        truth = []
        for label in per_class_test_results:
            test_results = per_class_test_results[label]
            n = len(test_results)

            for i in range(n):
                if(test_results[i]["correct_label"] != test_results[i]["predicted_label"]):
                    name = "misclassified_" + test_results[i]["predicted_label"]

                    img_summary_buffer = tf.summary.image(name, resized_image, 1)
                    jpg = gfile.FastGFile(test_results[i]["image_file_name"], "rb").read()
                    image_summary, _ = sess.run([img_summary_buffer, decoded_image], feed_dict={jpeg_data:jpg})
                    summary_writer.add_summary(image_summary)
            confidences, class_predictions, class_truth = self.extract_summary_tensors(test_results, label2idx)
            predictions.extend(class_predictions)
            truth.extend(class_truth)

            confidences_tensor = tf.placeholder(tf.float32, shape=(n,))
            confidences_summary_buffer = tf.summary.histogram('Confidences_' + label, confidences_tensor)

            # Summarize confidences in a multi-tiered histogram
            for i in range(c):
                confidences_summary = sess.run(confidences_summary_buffer, feed_dict={confidences_tensor: confidences[:,i]})
                summary_writer.add_summary(confidences_summary,i)

        # Confusion Matrix Plot
        cm = confusion_matrix(truth, predictions)

        classes = list(label2idx.keys())
        classes.sort()
        cm_img = self.plot_confusion_matrix(cm, classes=classes)
        summary_op = tf.summary.image("Confusion_Matrix", cm_img)
        confusion_summary = sess.run(summary_op)
        summary_writer.add_summary(confusion_summary)

        accuracy = self.compute_accuracy(cm)
        sensitivity, average_sensitivity = self.compute_sensitivity(cm)
        precision, average_precision = self.compute_precision(cm)

        prec_img = self.plot_bar(range(c), precision,  sensitivity  , title='Class Precision', xlabel='Class', ylabel='Precision and Sensitivity')
        summary_op = tf.summary.image("Precision", prec_img)
        prec_summary = sess.run(summary_op)
        summary_writer.add_summary(prec_summary)

        if print_results:
            print('Confusion Matrix: ', cm)
            print('Sensitivity: ', sensitivity)
            print('Average Sensitivity: ', average_sensitivity)
            print('Precision: ', precision)
            print('Average Precision: ', average_precision)
            print('Accuracy: ', accuracy)

        summary_writer.close()

        return {
            'Confusion Matrix':  cm,
            'Sensitivity': sensitivity,
            'Average Sensitivity': average_sensitivity,
            'Precision': precision,
            'Average Precision': average_precision,
            'Accuracy': accuracy,
        }

    def eval(self, output_folder, test_folder, test_result_file, test_result_path, notify_interval, input_dim):
        """
        Starting point of evaluation and run all other functions above
        :param output_folder: folder path to where the trained model is.
        :param test_result_path: path to the test dataset
        :param test_result_file: path to the pre-supplied test result file
        :param notify_interval: frequency of printing the progress of the evaluation
        :return: N/A
        """
        # Look at the folder structure, and create lists of all the images.
        label = os.path.join(output_folder, "labels.txt")

        # label_path is the same as output.txt
        label2idx, idx2label = self.create_label_lists(label)
        test_data = self.get_test_files(test_folder, label2idx, n=200)
        model_path = os.path.join(output_folder, "model.h5")
        model = load_model(model_path)

        inputShape = (input_dim, input_dim)
        preprocess = preprocess_input

        if test_result_file is None:
            per_class_test_results = {}
            for label in label2idx:

                per_class_test_results[label] = []

            count = 0

            for test_datum in test_data:
                if(count%notify_interval == 0):
                    print('processed {0}, {1} more to go'.format(count,len(test_data)-count) )

                test_result = {}

                # input
                image = load_img(test_datum[2], target_size=inputShape)
                # plt.savefig(os.path.join(folder_name, image))
                image = img_to_array(image)

                # our input image is now represented as a NumPy array of shape
                # (inputShape[0], inputShape[1], 3) however we need to expand the
                # dimension by making the shape (1, inputShape[0], inputShape[1], 3)
                # so we can pass it through thenetwork
                image = np.expand_dims(image, axis=0)

                # pre-process the image using the appropriate function based on the
                # model that has been loaded (i.e., mean subtraction, scaling, etc.)
                image = image/255.


                pred = model.predict(image)
                ground_truth = test_datum[1]

                # decode result tensor here since we don't have access to the prediction tensor
                test_result['prediction'], test_result['correct_label'], test_result['predicted_label'] , test_result['max_score']= \
                    self.eval_result(pred, ground_truth, idx2label)
                test_result['image_file_name'] = test_datum[2]
                test_result['class_confidences'] = pred
                per_class_test_results[test_result['correct_label']].append(test_result)

                count += 1
        else:
            print('Pre supplied test result file found, loading ... ')
            pickled_test_result = open(test_result_file,'rb')
            per_class_test_results = pickle.load(pickled_test_result)

        with tf.Session() as sess:
            summarized_results = self.summarize_results(sess ,label2idx, per_class_test_results, output_folder, print_results=True)

        with open(test_result_path, 'wb') as f:  # Python 3: open(..., 'wb')
            test_results = {
                'raw_test_results' : per_class_test_results,
                'summarized_results': summarized_results
            }
            pickle.dump(test_results, f)


keras_eval = KerasEval()

# Provide the path to each argument
keras_eval.eval(output_folder="/data/g1753002_ocado/manhattan_project/trained_models/resnet50_unfrozen/", \
                test_result_path="/data/g1753002_ocado/manhattan_project/trained_models/resnet50_unfrozen/training_results.pkl",
                test_result_file=None,
                test_folder='/data/g1753002_ocado/manhattan_project/test_data/extended_test_set_ambient',
                notify_interval=100,
                input_dim=224
)
