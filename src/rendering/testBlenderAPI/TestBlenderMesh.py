# This is a script for testing functions in the BlenderMesh class found in the file BlenderShapes.py

import bpy

import sys

boop = '/Users/matthew/Documents/MSc/Group_Project/Lobster/src/'
if not (boop in sys.path):
    sys.path.append(boop)

C = bpy.context
C.scene.render.engine = 'CYCLES'


import unittest


import rendering.BlenderAPI as bld


from rendering.BlenderAPI.BlenderScene import BlenderScene
from rendering.BlenderAPI.BlenderScene import BlenderRoom
from rendering.BlenderAPI.BlenderCamera import BlenderCamera
from rendering.BlenderAPI.BlenderLamps import BlenderLamp, BlenderSun
from rendering.BlenderAPI.BlenderShapes import *

class BlenderMeshTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        self.my_cube = BlenderCube()
        self.my_cube_nodes = bpy.data.objects['Cube'].data.materials[0].node_tree.nodes

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_set_diffuse(self):
        test_colors = [0.5, 0.5, 0.5, 1.0]
        colors = self.my_cube_nodes["Diffuse BSDF"].inputs["Color"].default_value
        roughness = self.my_cube_nodes["Diffuse BSDF"].inputs["Roughness"].default_value

        # At this point all values should still be set to their default
        self.assertNotEqual(list(colors), test_colors)
        self.assertNotEqual(roughness, 0.5)

        # Setting diffuse, which will change the values for colour and roughness
        self.my_cube.set_diffuse();
        colors = self.my_cube_nodes["Diffuse BSDF"].inputs["Color"].default_value
        roughness = self.my_cube_nodes["Diffuse BSDF"].inputs["Roughness"].default_value

        # # Now the values should be changed to that which we have set them to
        self.assertEqual(list(colors), test_colors)
        self.assertEqual(roughness, 0.5)

    def test_set_gloss(self):
        test_colors = [0.5, 0.5, 0.5, 1.0]
        colors = self.my_cube_nodes["Glossy BSDF"].inputs["Color"].default_value
        roughness = self.my_cube_nodes["Glossy BSDF"].inputs["Roughness"].default_value

        # At this point all values should still be set to their default
        self.assertNotEqual(list(colors), test_colors)
        self.assertNotEqual(roughness, 0.5)

        # Setting gloss, which will change the values for colour and roughness
        self.my_cube.set_gloss();
        colors = self.my_cube_nodes["Glossy BSDF"].inputs["Color"].default_value
        roughness = self.my_cube_nodes["Glossy BSDF"].inputs["Roughness"].default_value

        # Now the values should be changed to that which we have set them to
        self.assertEqual(list(colors), test_colors)
        self.assertEqual(roughness, 0.5)

    def test_set_mix(self):
        fac = self.my_cube_nodes["Mix Shader"].inputs["Fac"].default_value

        # At this point all values should still be set to their default
        self.assertNotEqual(fac, 0.9)

        # Setting mixer, which will change the values for colour and roughness
        self.my_cube.set_mixer(0.9);
        fac = self.my_cube_nodes["Mix Shader"].inputs["Fac"].default_value

        # Now the values should be changed to that which we have set them to
        self.assertAlmostEqual(fac, 0.9)


if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
