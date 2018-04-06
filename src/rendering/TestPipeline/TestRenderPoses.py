import pathlib
import sys
import os
import unittest
import shutil

import bpy 

# sys.path.append("/Users/maxbaylis/Lobster/src/")

import rendering.BlenderAPI as bld

from rendering.render_poses import find_model

class TestRenderPoses(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('dummy_dir', ignore_errors=True)               
        os.mkdir('dummy_dir')

    def tearDown(self):
        shutil.rmtree('dummy_dir', ignore_errors=True)

    def test_find_model(self):
        # create an empty .model file
        os.mknod(os.path.join('dummy_dir', 'dummy.model'))
        filename = find_model('dummy_dir')
        self.assertEqual('dummy.model', filename)

if __name__=='__main__':
    unittest.main()
      