# For the relative path to work, you have to append the absolute path of your comment
import sys
sys.path.append("/homes/kk3317/Desktop/Ocado/Lobster/src")

from tensorflow.python.framework import test_util
import tensorflow as tf

import os

current_dir = os.path.dirname(os.path.realpath(__file__))

from kerasmodels.keras_eval import *
from kerasmodels.keras_eval_errors import *
import kerasmodels.keras_eval as test

class KerasEvalTest(test_util.TensorFlowTestCase):
    def test_create_label_lists(self):
        keras_eval = KerasEval()
        # Case 1: Correct path
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = keras_eval.create_label_lists(label_path)
        self.assertEqual({'apple': 0, 'banana': 1}, label2idx)
        self.assertEqual({0: 'apple', 1: 'banana'}, idx2label)
        # Case 2: Incorrect path
        caught = False
        try:
            label_path = os.path.join("/", "test.txt")
            keras_eval.create_label_lists(label_path)
        except FileNotFoundError:
            caught = True
        self.assertTrue(caught)

    def test_get_test_files(self):
        keras_eval = KerasEval()
        # Case1: Correct folder structure
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = keras_eval.create_label_lists(label_path)
        filedir = os.path.join(current_dir, "test_images")
        test_files = keras_eval.get_test_files(filedir, label2idx, 1)
        self.assertEqual([('banana', 1, os.path.join(filedir, 'banana','trump.jpg'))], test_files)

        # Case 2: Incorrect folder structure
        caught = False
        try:
            label_path = os.path.join(current_dir, "test.txt")
            label2idx, idx2label = keras_eval.create_label_lists(label_path)
            filedir = os.path.join(current_dir, "hidden_folder")
            test_files = keras_eval.get_test_files(filedir, label2idx, 1)
        except InvalidDirectoryStructureError:
            caught = True
        self.assertTrue(caught)

    def test_eval_result(self):
        keras_eval = KerasEval()
        # Case 1: eval_result() predicts correctly
        result_tensor = [[0.5180032,  0.4819968]]
        ground_truth = 0
        idx2label = {0: 'yogurt', 1: 'cheese'}
        prediction, correct_label, predicted_label, max_score = keras_eval.eval_result(result_tensor, ground_truth, idx2label)
        self.assertEqual(True, prediction)
        self.assertEqual('yogurt', correct_label)
        self.assertEqual('yogurt', predicted_label)
        self.assertGreaterEqual(max_score, 0)
        self.assertLessEqual(max_score, 1)
        # Case 2: eval_result() predicts incorrectly
        result_tensor = [[0.1,  0.9]]
        ground_truth = 0
        idx2label = {0: 'yogurt', 1: 'cheese'}
        prediction, correct_label, predicted_label, max_score = keras_eval.eval_result(result_tensor, ground_truth, idx2label)
        self.assertFalse(prediction)
        self.assertEqual('yogurt', correct_label)
        self.assertEqual('cheese', predicted_label)
        self.assertGreaterEqual(max_score, 0)
        self.assertLessEqual(max_score, 1)
        # Case 3: result_tensor is incorrect
        caught = False
        try:
            result_tensor = [[0.1, 0.91]]
            prediction, correct_label, predicted_label, max_score = keras_eval.eval_result(result_tensor, ground_truth, idx2label)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
    def test_extract_summary_tensors(self):
        keras_eval = KerasEval()
        # No need to do partition test
        test_results = [
            {'class_confidences' : np.array([[0.6, 0.4]]), 'predicted_label': '0', 'correct_label': '1'},
            {'class_confidences' : np.array([[0.51, 0.49]]), 'predicted_label': '0', 'correct_label': '1'},
        ]
        label2idx = {'0':0, '1':1}
        confidences, predictions, truth = keras_eval.extract_summary_tensors(test_results, label2idx)
        self.assertAllEqual(confidences, np.array([[0.6, 0.4],[0.51, 0.49]]))
        self.assertAllEqual(predictions, np.array([0,0]))
        self.assertAllEqual(truth, np.array([1,1]))
    def test_plot_confusion_matrix(self):
        keras_eval = KerasEval()
        # square confusion matrix
        cm = np.array([[1,0],[0,1]])
        image = keras_eval.plot_confusion_matrix(cm, ['0','1'])
        self.assertIsNotNone(image)
        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            keras_eval.plot_confusion_matrix(cm, ['0', '1'])
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
        # wrong number of classes
        cm = np.array([[1, 0], [0, 1]])
        caught = False
        try:
            image = keras_eval.plot_confusion_matrix(cm, ['0', '1', '2'])
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
    def test_compute_sensitivity(self):
        keras_eval = KerasEval()
        # case 1 class
        cm = np.array([[1]])
        sens = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1.]))
        # case 2 classes
        cm = np.array([[1,0],[0,1]])
        sens = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1., 1.]))
        cm = np.array([[1,1],[0,1]])
        sens = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([.5, 1.]))
        # case one empty class
        cm = np.array([[1, 1], [0, 0]])
        sens = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([.5, -1]))
        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            keras_eval.compute_sensitivity(cm)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
    def test_compute_precision(self):
        keras_eval = KerasEval()
	# case 1 class
        cm = np.array([[1]])
        prec = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1.]))
        # case 2 classes
        cm = np.array([[1,0],[0,1]])
        prec = keras_eval.compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1., 1.]))
        cm = np.array([[1,1],[0,1]])
        prec = keras_eval.compute_precision(cm)
        self.assertAllClose(prec, np.array([1., .5]))
        # case one empty class
        cm = np.array([[0, 1], [0, 1]])
        prec = keras_eval.compute_precision(cm)
        self.assertAllClose(prec, np.array([-1, .5]))
        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            keras_eval.compute_sensitivity(cm)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
    def test_summarize_results(self):
        keras_eval = KerasEval()
        label2idx = {'0':0, '1':1}
        dummy_image = os.path.join(current_dir, "test_images", "banana", "trump.jpg")
        per_class_test_results = {
            '1':[{'class_confidences' : np.array([[0.6, 0.4]]), 'predicted_label': '0', 'correct_label': '1', 'image_file_name': dummy_image},],
            '1':[{'class_confidences' : np.array([[0.51, 0.49]]), 'predicted_label': '0', 'correct_label': '1', 'image_file_name': dummy_image}]
        }
        model_source_dir = os.path.join(current_dir, "outputs/")
        with tf.Session() as sess:
            keras_eval.summarize_results(sess, label2idx, per_class_test_results, model_source_dir)
            self.assertTrue(tf.gfile.Exists(model_source_dir + '/test_results'))
            tf.gfile.DeleteRecursively(model_source_dir + '/test_results')
    # def test_eval(self):
    #     keras_eval = KerasEval()
    #     keras_eval.eval(output_folder="/vol/project/2017/530/g1753002/Trained_Models", \
    #                     test_result_path="/vol/project/2017/530/g1753002/training_results.pkl",
    #                     test_result_file=None,
    #                     test_folder='/vol/project/2017/530/g1753002/matthew/8_class_data/qlone_training_images/',
    #                     notify_interval=1000,
    #                     input_dim=224
    #     )
    #
    #     model_source_dir = "/vol/project/2017/530/g1753002/output"
    #     self.assertTrue(tf.gfile.Exists(model_source_dir + '/test_results'))
    #     tf.gfile.DeleteRecursively(model_source_dir + '/test_results')
tf.test.main()
