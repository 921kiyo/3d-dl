# TODO For the relative path to work, you have to append the absolute path of your comment
# import sys
# print("Sys.path ", sys.path)
# sys.path.append("/homes/kk3317/Desktop/Ocado/Lobster/src")
from tensorflow.python.framework import test_util
import tensorflow as tf

import os

current_dir = os.path.dirname(os.path.realpath(__file__))

from image_retraining.test import *
import image_retraining.test as test

class TestTest(test_util.TensorFlowTestCase):
    def test_create_label_lists(self):
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = create_label_lists(label_path)
        self.assertEqual({'apple': 0, 'banana': 1}, label2idx)
        self.assertEqual({0: 'apple', 1: 'banana'}, idx2label)
        pass

    def test_get_test_files(self):
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = create_label_lists(label_path)
        filedir = os.path.join(current_dir, "test_images/")
        test_files = get_test_files(filedir, label2idx, 1)
        self.assertEqual([('banana', 1, os.path.join(current_dir, '/banana/trump.jpg'))], test_files)
        pass

    def test_create_model_graph(self):
        path = "/"
        model_info = create_model_info(path)
        graph, resized_input_tensor, bottleneck_tensor, result_tensor = create_model_graph(model_info)
        self.assertIsNotNone(graph)
        self.assertIsNotNone(resized_input_tensor)
        self.assertIsNotNone(bottleneck_tensor)
        self.assertIsNotNone(result_tensor)

    def test_create_model_info(self):
        path = "/"
        model_info = create_model_info(path)
        self.assertEqual(path, model_info['data_url'])
        self.assertEqual("final_result:0", model_info['result_tensor_name'])
        self.assertEqual("Mul:0", model_info['resized_input_tensor_name'])
        self.assertEqual("output_graph.pb", model_info['model_file_name'])
        self.assertEqual("pool_3/_reshape:0", model_info['bottleneck_tensor_name'])
        self.assertEqual(2048, model_info['bottleneck_tensor_size'])
        self.assertEqual(299, model_info['input_width'])
        self.assertEqual(299, model_info['input_height'])
        self.assertEqual(3, model_info['input_depth'])
        self.assertEqual(128, model_info['input_mean'])
        self.assertEqual(128, model_info['input_std'])
        pass

    def test_add_jpeg_decoding(self):
        with tf.Graph().as_default():
            jpeg_data, mul_image, decoded_image = add_jpeg_decoding(10, 10, 3, 0, 255)
            self.assertIsNotNone(jpeg_data)
            self.assertIsNotNone(mul_image)
            self.assertIsNotNone(decoded_image)

    def test_run_resize_data(self):        # Build jpeg decoding and give it to run resized data
        with tf.Graph().as_default():
            with tf.Session() as sess:
                jpeg_data, mul_image, decoded_image = add_jpeg_decoding(10, 10, 3, 0, 255)
                label_path = os.path.join(current_dir, "test.txt")
                label2idx, idx2label = create_label_lists(label_path)
                file_dir = os.path.join(current_dir, "test_images/")
                test_data = get_test_files(file_dir, label2idx, 1)
                self.assertTrue(len(test_data) > 0)
                for test_datum in test_data:
                    image_data = gfile.FastGFile(test_datum[2], 'rb').read()
                    resized_input_values, decoded_jpeg_data = run_resize_data(sess, image_data, jpeg_data, mul_image, decoded_image)
                    self.assertIsNotNone(resized_input_values)
                    self.assertIsNotNone(decoded_jpeg_data)
        pass

    def test_eval_result(self):
        result_tensor = [[0.5180032,  0.48199683]]
        ground_truth = 0
        idx2label = {0: 'yogurt', 1: 'cheese'}
        prediction, correct_label, predicted_label = eval_result(result_tensor, ground_truth, idx2label)
        self.assertEqual(True, prediction)
        self.assertEqual('yogurt', correct_label)
        self.assertEqual('yogurt', predicted_label)
        pass

    def test_extract_summary_tensors(self):
        test_results = [
            {'class_confidences' : np.array([[0.6, 0.4]]), 'predicted_label': '0', 'correct_label': '1'},
            {'class_confidences' : np.array([[0.51, 0.49]]), 'predicted_label': '0', 'correct_label': '1'},
        ]
        label2idx = {'0':0, '1':1}
        confidences, predictions, truth = extract_summary_tensors(test_results, label2idx)
        self.assertAllEqual(confidences, np.array([[0.6, 0.4],[0.51, 0.49]]))
        self.assertAllEqual(predictions, np.array([0,0]))
        self.assertAllEqual(truth, np.array([1,1]))
        pass

    def test_plot_confusion_matrix(self):
        cm = np.array([[1,0],[0,1]])
        image = plot_confusion_matrix(cm, ['0','1'])
        self.assertIsNotNone(image)
        pass

    def test_get_test_files(self):
        with tf.Graph().as_default():
            with tf.Session() as sess:
                jpeg_data, mul_image, decoded_image = add_jpeg_decoding(10, 10, 3, 0, 255)
                label_path = os.path.join(current_dir, "test.txt")
                label2idx, idx2label = create_label_lists(label_path)
                file_dir = os.path.join(current_dir, "test_images/")
                test_data = get_test_files(file_dir, label2idx, 1)
                self.assertTrue(len(test_data) > 0)
        pass

    def test_compute_sensitivity(self):

        cm = np.array([[1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1.]))

        cm = np.array([[1,0],[0,1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1., 1.]))

        cm = np.array([[1,1],[0,1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([.5, 1.]))
        pass

    def test_compute_precision(self):

        cm = np.array([[1]])
        prec = compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1.]))

        cm = np.array([[1,0],[0,1]])
        prec = compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1., 1.]))

        cm = np.array([[1,1],[0,1]])
        prec = compute_precision(cm)
        self.assertAllClose(prec, np.array([1., .5]))

        pass

    def test_plot_bar(self):
        # Ong
        pass

    @tf.test.mock.patch.object(test, 'FLAGS', model_source_dir=os.path.join(current_dir, "outputs/"))
    def test_summarize_results(self, flags_mock):

        label2idx = {'0':0, '1':1}
        per_class_test_results = {
            '1':[{'class_confidences' : np.array([[0.6, 0.4]]), 'predicted_label': '0', 'correct_label': '1'},],
            '1':[{'class_confidences' : np.array([[0.51, 0.49]]), 'predicted_label': '0', 'correct_label': '1'}]
        }

        with tf.Session() as sess:
            test.summarize_results(sess, label2idx, per_class_test_results)
            self.assertTrue(tf.gfile.Exists(test.FLAGS.model_source_dir + '/test_results'))
            tf.gfile.DeleteRecursively(test.FLAGS.model_source_dir + '/test_results')
        pass

if __name__ == '__main__':
  tf.test.main()
