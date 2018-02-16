from tensorflow.python.framework import test_util
import tensorflow as tf
from test import *

# import uunitest

# 15 unit tests

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
        # Ong
        pass

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
        # Ong
        pass

    def test_plot_confusion_matrix(self):
        # Ong
        pass

    def test_get_test_files(self):
        # Kiyo
        pass

    def test_compute_sensitivity(self):
        # Ong
        pass

    def test_compute_precision(self):
        # Ong
        pass

    def test_plot_bar(self):
        # Ong
        pass

    def test_summarize_results(self):
        # Ong
        pass

if __name__ == '__main__':
  tf.test.main()
