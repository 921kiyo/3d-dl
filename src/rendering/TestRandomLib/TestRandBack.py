# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 09:35:54 2018

@author: Pavel

Tests function in random_background.py
Since these tests are based on random functions
or random number generators, each function is tested several
times to ensure that it behaves correctly.
"""


import unittest

import os, sys
from PIL import Image
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(dir_path, os.pardir))
base_path = os.path.abspath(os.path.join(parent,os.pardir)) # folder /src

if not (base_path in sys.path):
    sys.path.append(base_path)

import rendering.RandomLib.random_background as rb

n_of_tests = 5
class TestResizeImages(unittest.TestCase):
    
    def test_random_color(self):
        """
        Tests that returns a L*L*3 array of values between 0 and1
        """
        for i in range(n_of_tests):
            result = rb.random_color(300)
            self.assertEqual((300,300,3), np.shape(result))
            for color in result:
                for line in color:
                    for value in line:
                        self.assertTrue(value>=0 and value <=2.0)
                        
    def test_random_image(self):
        """
        Test random_image by checking that the resultant image
        is size*size*3 array of values between 0 and 2? for now,
        Ong will solve the problem
        """
        
        for i in range(n_of_tests):
            result = rb.random_image(300)
            self.assertEqual((300,300,3), np.shape(result))
            for color in result:
                for line in color:
                    for value in line:
                        self.assertTrue(value>=0 and value <=2.0)
    
    
    def test_mix(self):
        """
        Test that return array is size*size*3
        this mixes the images with metaballs
        It would be good to test what happens when images of wrong
        size are passed
        """                        
        for i in range(n_of_tests):
            img1 = rb.random_image(300)
            img2 = rb.random_image(300)
            result = rb.mix(img1, img2,300)
            self.assertEqual((300,300,3), np.shape(result))
            for color in result:
                for line in color:
                    for value in line:
                        self.assertTrue(value>=0 and value <=2.0)
        
            
    def test_rand_background(self):
        """
        Creates a single image of size*size*3 by merging N
        random images. Usually use between 2 and 3 layers
        """
        
        for i in range(n_of_tests):
        
            result = rb.rand_background(4,300)
            self.assertEqual((300,300,3), np.shape(result))
            for color in result:
                for line in color:
                    for value in line:
                        self.assertTrue(value>=0 and value <=2.0)
                        
    
    def test_generate_images(self):
        """
        Generates few images, checks that they are of the
        correct size and values and saves them
        """
        
        
        master_path = os.path.abspath(os.path.join(base_path, os.pardir))
        test_path = os.path.join(master_path, 'test_data', 'rendering_tests', 'rand_back')
        
        # Clean the folder
        for the_file in os.listdir(test_path):
            file_path = os.path.join(test_path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        self.assertEqual(0, len(os.listdir(test_path)))  
        
        
        rb.generate_images(test_path, 300, 0,5)
        all_images = os.listdir(test_path)
        self.assertEqual(5, len(all_images))
        
        for the_file in os.listdir(test_path):
            file_path = os.path.join(test_path, the_file)
            with Image.open(file_path) as f:
                self.assertEqual(300, f.size[0])
                self.assertEqual(300, f.size[1])

if __name__=='__main__':
    unittest.main()