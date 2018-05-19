import unittest
from shutil import copyfile
from PIL import Image

import os.path

import flask_implementations

from keras.models import load_model

class TestFlaskImplementations(unittest.TestCase):

    def test_generate_unique_filepath(self):
        filepath_1 = flask_implementations.generate_unique_filepath('')
        filepath_2 = flask_implementations.generate_unique_filepath('')
        print (' ')
        print(filepath_1, filepath_2)
        self.assertNotEqual(filepath_1, filepath_2)

    def test_crop_image(self):
        # Change these paths as necessary
        my_path = os.path.abspath(os.path.dirname(__file__))
        original_path = str(my_path) + '/test_image.jpg'
        target_path = str(my_path) + '/temp_test.jpg'
        copyfile(original_path, target_path)
        flask_implementations.crop_image('/temp_test.jpg')

        im = Image.open(target_path)
        width, height = im.size

        self.assertEqual(width, height)

    def test_get_predictions(self):
        # Change to location of your model
        model = load_model('/data/g1753002_ocado/manhattan_project/trained_models/first_attempt_with_all_layers_unfrozen/model.h5')
        # Change this as necessary
        predictions = flask_implementations.get_predictions('/temp_test.jpg', model)
        print(predictions.shape)
        print(predictions[0].shape)
        self.assertEqual(predictions.shape, (1,10))
        self.assertEqual(predictions[0].shape, (10,))


    def test_process_predictions(self):
        # Array of sample predictions - corresponds to Anchor being the max class with 99.5% accuracy
        predictions = [[0.995, 0.005, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000]]

        result = flask_implementations.process_predictions(predictions)

        print(result)

        self.assertEqual(result['max_class'], "Anchor")
        self.assertEqual(result['max_value'], "99.5")




if __name__ == '__main__':
    unittest.main()
