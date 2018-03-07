# For the relative path to work, you have to append the absolute path of your comment
# import sys
# sys.path.append("/homes/kk3317/Desktop/Ocado/Lobster/src")

from tensorflow.python.framework import test_util
import tensorflow as tf

import os

current_dir = os.path.dirname(os.path.realpath(__file__))

from image_retraining.test import *
from image_retraining.test_errors import *
import image_retraining.test as test

class TestTest(test_util.TensorFlowTestCase):
    def test_create_label_lists(self):
        # Case 1: Correct path
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = create_label_lists(label_path)
        self.assertEqual({'apple': 0, 'banana': 1}, label2idx)
        self.assertEqual({0: 'apple', 1: 'banana'}, idx2label)
        # Case 2: Incorrect path
        caught = False
        try:
            label_path = os.path.join("/", "test.txt")
            create_label_lists(label_path)
        except FileNotFoundError:
            caught = True
        self.assertTrue(caught)

    def test_get_test_files(self):
        # Case1: Correct folder structure
        label_path = os.path.join(current_dir, "test.txt")
        label2idx, idx2label = create_label_lists(label_path)
        filedir = os.path.join(current_dir, "test_images")
        test_files = get_test_files(filedir, label2idx, 1)
        self.assertEqual([('banana', 1, os.path.join(filedir, 'banana','trump.jpg'))], test_files)

        # Case 2: Incorrect folder structure
        caught = False
        try:
            label_path = os.path.join(current_dir, "test.txt")
            label2idx, idx2label = create_label_lists(label_path)
            filedir = os.path.join(current_dir, "hidden_folder")
            test_files = get_test_files(filedir, label2idx, 1)
        except InvalidDirectoryStructureError:
            caught = True
        self.assertTrue(caught)

    def test_create_model_info(self):
        # No need to do partition test
        model_info = create_model_info(current_dir)
        self.assertEqual(current_dir, model_info['data_url'])
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

    def test_create_model_graph(self):
        # Case1: correct path
        model_info = create_model_info(current_dir)
        graph, resized_input_tensor, bottleneck_tensor, result_tensor = create_model_graph(model_info)
        self.assertIsNotNone(graph)
        self.assertIsNotNone(resized_input_tensor)
        self.assertIsNotNone(bottleneck_tensor)
        self.assertIsNotNone(result_tensor)
        # Case 2: Incorrect path
        caught = False
        try:
            model_info = create_model_info("/")
            create_model_graph(model_info)
        except tf.errors.NotFoundError:
            caught = True
        self.assertTrue(caught)

    def test_add_jpeg_decoding(self):
        with tf.Graph().as_default():
            # test correct inputs
            jpeg_data, mul_image, decoded_image = add_jpeg_decoding(10, 10, 3, 0, 255)
            self.assertIsNotNone(jpeg_data)
            self.assertIsNotNone(mul_image)
            self.assertIsNotNone(decoded_image)
            self.assertEqual(mul_image.shape, (1,10,10,3))

            # test incorrect inputs
            caught = False
            try:
                add_jpeg_decoding(-10, 10, 3, 0, 255)
            except InvalidInputError:
                caught = True
            self.assertTrue(caught)

    def test_run_resize_data(self):        # Build jpeg decoding and give it to run resized data
        # No need to do partition test
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
        # Case 1: eval_result() predicts correctly
        result_tensor = [[0.5180032,  0.4819968]]
        ground_truth = 0
        idx2label = {0: 'yogurt', 1: 'cheese'}
        prediction, correct_label, predicted_label = eval_result(result_tensor, ground_truth, idx2label)
        self.assertEqual(True, prediction)
        self.assertEqual('yogurt', correct_label)
        self.assertEqual('yogurt', predicted_label)

        # Case 2: eval_result() predicts incorrectly
        result_tensor = [[0.1,  0.9]]
        ground_truth = 0
        idx2label = {0: 'yogurt', 1: 'cheese'}
        prediction, correct_label, predicted_label = eval_result(result_tensor, ground_truth, idx2label)
        self.assertFalse(prediction)
        self.assertEqual('yogurt', correct_label)
        self.assertEqual('cheese', predicted_label)

        # Case 3: result_tensor is incorrect
        caught = False
        try:
            result_tensor = [[0.1, 0.91]]
            prediction, correct_label, predicted_label = eval_result(result_tensor, ground_truth, idx2label)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
        pass

    def test_extract_summary_tensors(self):
        # No need to do partition test
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
        # square confusion matrix
        cm = np.array([[1,0],[0,1]])
        image = plot_confusion_matrix(cm, ['0','1'])
        self.assertIsNotNone(image)

        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            plot_confusion_matrix(cm, ['0', '1'])
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

        # wrong number of classes
        cm = np.array([[1, 0], [0, 1]])
        caught = False
        try:
            image = plot_confusion_matrix(cm, ['0', '1', '2'])
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)
        pass

    def test_compute_sensitivity(self):

        # case 1 class
        cm = np.array([[1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1.]))

        # case 2 classes
        cm = np.array([[1,0],[0,1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([1., 1.]))

        cm = np.array([[1,1],[0,1]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([.5, 1.]))

        # case one empty class
        cm = np.array([[1, 1], [0, 0]])
        sens = compute_sensitivity(cm)
        self.assertAllClose(sens, np.array([.5, -1]))

        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            compute_sensitivity(cm)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

        pass

    def test_compute_precision(self):

        # case 1 class
        cm = np.array([[1]])
        prec = compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1.]))

        # case 2 classes
        cm = np.array([[1,0],[0,1]])
        prec = compute_sensitivity(cm)
        self.assertAllClose(prec, np.array([1., 1.]))

        cm = np.array([[1,1],[0,1]])
        prec = compute_precision(cm)
        self.assertAllClose(prec, np.array([1., .5]))

        # case one empty class
        cm = np.array([[0, 1], [0, 1]])
        prec = compute_precision(cm)
        self.assertAllClose(prec, np.array([-1, .5]))

        # non-square confusion matrix
        cm = np.array([[1, 0, 0], [0, 1, 0]])
        caught = False
        try:
            compute_sensitivity(cm)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

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
