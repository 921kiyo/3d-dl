from tensorflow.python.framework import test_util
import tensorflow as tf
from test import *
import test


class TestTest(test_util.TensorFlowTestCase):
    def test_create_label_lists(self):
        label_path = "//"
        # result = create_label_lists(label_path)
        self.assertEqual(True, True)
        # Kiyo
        # txt.file chees yougurlt
        # label2index {"yogurt": 1 }
        pass

    def test_get_test_files(self):
        # Kiyo
        pass

    def test_create_model_graph(self):
        # Kiyo
        path = "/vol/project/2017/530/g1753002/tmp"
        model_info = create_model_info(FLAGS.model)
        pass

    def test_create_model_info(self):
        # Kiyo
        pass

    # def test_run_resize_data(self):
    #     # Kiyo
    #     pass

    # def test_adaptive_equalize(self):
    #     # Kiyo
    #     pass
    #
    # def test_tf_equalize(self):
    #     # Kiyo
    #     pass

    def test_add_jpeg_decoding(self):
        with tf.Graph().as_default():
            jpeg_data, mul_image, decoded_image = add_jpeg_decoding(10, 10, 3, 0, 255)
            self.assertIsNotNone(jpeg_data)
            self.assertIsNotNone(mul_image)
            self.assertIsNotNone(decoded_image)

    def test_run_resize_data(self):
        # Kiyo
        # Build jpeg decoding and give it to run resized data
        #
        pass

    def test_eval_result(self):
        # Kiyo
        # result_tensor is numpy array, ground_truth scalar between 0 and N-1
        # N is the length of result tensor softmax confidence, highest
        # prediction is boolean value true if argmax(result_tensor) == ground_truth
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
        # Kiyo
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

    @tf.test.mock.patch.object(test, 'FLAGS', model_source_dir='./')
    def test_summarize_results(self, flags_mock):
        
        label2idx = {'0':0, '1':1}
        per_class_test_results = {
            '0':[{'class_confidences' : np.array([[0.6, 0.4]]), 'predicted_label': '0', 'correct_label': '1'},],
            '1':[{'class_confidences' : np.array([[0.51, 0.49]]), 'predicted_label': '0', 'correct_label': '1'}]
        }
        
        with tf.Session() as sess:
            test.summarize_results(sess, label2idx, per_class_test_results)
            self.assertTrue(tf.gfile.Exists(test.FLAGS.model_source_dir + '/test_results'))
            tf.gfile.DeleteRecursively(test.FLAGS.model_source_dir + '/test_results')
        pass

if __name__ == '__main__':
  tf.test.main()
