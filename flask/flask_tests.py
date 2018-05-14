import unittest
from shutil import copyfile
from PIL import Image

import flask_implementations

class TestFlaskImplementations(unittest.TestCase):

    def test_generate_unique_filepath(self):
        filepath_1 = flask_implementations.generate_unique_filepath('')
        filepath_2 = flask_implementations.generate_unique_filepath('')
        print (' ')
        print(filepath_1, filepath_2)
        self.assertNotEqual(filepath_1, filepath_2)

    def test_crop_image(self):
        copyfile('test_image.jpg', 'temp_test.jpg')
        flask_implementations.crop_image('temp_test.jpg')

        im = Image.open('temp_test.jpg')
        width, height = im.size

        self.assertEqual(width, height)

    def test_get_predictions(self):
        self.assertEqual(1, 1)

    def test_process_predictions(self):
        # Array of sample predictions - corresponds to Anchor being the max class with 99.5% accuracy
        predictions = [[0.995, 0.005, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000]]

        result = flask_implementations.process_predictions(predictions)

        # print(flask_implementations.process_predictions(predictions))

        print(result)

        self.assertEqual(result['max_class'], "Anchor")
        self.assertEqual(result['max_value'], "99.5")




if __name__ == '__main__':
    unittest.main()
