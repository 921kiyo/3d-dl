# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:50:43 2018

@author: Pavel

Contains tests for the files: 
    Resize_background.py
    Merge_images.py
    
Most of these tests creates some images.
These images are deleted not at the end of the run, 
but at the start of the next.
The reason is that a visual inspection of the results is also a good
way of testing the functions.

"""

import unittest


import os,io, sys
from PIL import Image


dir_path = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(dir_path, os.pardir))
gr_parent = os.path.abspath(os.path.join(parent,os.pardir))
base_path = os.path.abspath(os.path.join(gr_parent,os.pardir))

if not (parent in sys.path):
    sys.path.append(parent)
    
import SceneLib.Resize_background as rb
import SceneLib.Merge_Images as mi

#base_path = 'D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/test_data/'

class TestResizeImages(unittest.TestCase):
    
    def test_full_resize(self):
        """
        should find seven images and resize them.
        One of them is too small and so should be ignored
        Final folder should have 6 images
        Tests that all images are found in any subfolder
        That too small images are ignored
        And the remaining images are of the right format
        """
        number_of_pixels = 300
        destination = base_path +'/test_data/rendering_tests/resized_images/'
        source_folder = base_path + '/test_data/rendering_tests/filter_database/'
        
        
        for the_file in os.listdir(destination):
            file_path = os.path.join(destination, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        
        self.assertEqual(0, len(os.listdir(destination)))
        rb.find_all_files(number_of_pixels,source_folder, destination)
        self.assertEqual(6, len(os.listdir(destination)))
        for the_file in os.listdir(destination):
            file_path = os.path.join(destination,the_file)
            with Image.open(file_path) as f:
                self.assertNotEqual(number_of_pixels+5, f.size[0])
                self.assertNotEqual(number_of_pixels+5, f.size[1])
                # the above checks that the size does not vary as needed
                # probably not necessary
                self.assertEqual(number_of_pixels, f.size[0])
                self.assertEqual(number_of_pixels, f.size[1])
                

    def test_single_resize_er(self):
        """
        Tries to resize single image but the image is too small.
        Thus prints error message that is captured and compared to expected message
        First it deletes any file in the output folder.
        """
        to_resize = base_path + '/test_data/rendering_tests/just_resize/original/faulty.jpg'
        to_output = base_path + '/test_data/rendering_tests/just_resize/results/'
        
        for the_file in os.listdir(to_output):
            file_path = os.path.join(to_output, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        rb.resize_and_crop(to_resize, to_output+"faulty.jpg", 300,300 )
        sys.stdout = sys.__stdout__                     # Reset redirect.
        self.assertEqual("Image too small to be resized\n",capturedOutput.getvalue())   # Now works as before.
         
        
    def test_single_resize_ok(self):
        """
        Resize and crop single image succesfully.
        After doing so, checks that there is exactly one image present.
        First it deletes any file in the output folder.
        """
    
        to_resize = base_path +'/test_data/rendering_tests/just_resize/original/good.jpg'
        to_output = base_path +'/test_data/rendering_tests/just_resize/results/'
 
        for the_file in os.listdir(to_output):
            file_path = os.path.join(to_output, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    
        rb.resize_and_crop(to_resize, to_output+"good.jpg", 300,300 )
        self.assertEqual(1, len(os.listdir(to_output)))
        
    def test_single_merge(self):
        """
        This function will test merge of two images.
        Checks that the file is created and is of the right resolution
        and format (e.g. .jpg extension)
        At start, it deletes any previously created file 
        (e.g. created during previous run)
        The pixels are not exactly the same as the function used for merge 
        somehow changes the pixels by one or two 
        So cannot just compare all the pixels
        """
        test_folder = base_path +'/test_data/merging_tests/single_test/'
        # the files are: render1.png and background.jpg
        output_file = os.path.join(test_folder, "output1.jpg")
        if(os.path.isfile(output_file)):
            os.unlink(output_file) 
        
        mi.add_background(test_folder+"render1.png", test_folder+"background.jpg", output_file)
        self.assertTrue(os.path.isfile(output_file))
        output = Image.open(output_file)
        self.assertEqual((300,300),output.size)
        self.assertEqual('JPEG',output.format)
        
    def test_all_merge(self):
        """
        Tests the generate_for_all_objects function
        Checks that a corresponding image is created for each object_pose
        It checks that each file has the right resolution and extension
        Also uses different background images to the test_single_merge
        as it uses the randomly python generated images.
        These backgrounds are .png which is different from the other test function
        
        """
        
        test_folder = base_path + '/test_data/merging_tests/batch_test/'
        results_folder = test_folder+"results/"
        # delete all files in output folder
        for the_file in os.listdir(results_folder):
            file_path = os.path.join(results_folder, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                
        mi.generate_for_all_objects(test_folder+"object_poses/", test_folder+"backgrounds", results_folder)
        self.assertEqual(len(os.listdir(test_folder+"object_poses")), len(os.listdir(results_folder)))
        
        for the_file in os.listdir(results_folder):
            file_path = os.path.join(results_folder, the_file)
            im = Image.open(file_path)
            self.assertEqual((300,300), im.size)
            self.assertEqual('JPEG', im.format)
            self.assertNotEqual('PNG', im.format)
            
        


if __name__=='__main__':
    unittest.main()
