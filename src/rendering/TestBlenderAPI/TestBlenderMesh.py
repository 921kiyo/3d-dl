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
        caught = False
        try:
            self.my_cube.set_diffuse(color=(0.5, 0.5, -0.1, 2.0))
        except InvalidInputError:
            caught = True
        try:
            self.my_cube.set_diffuse(rough=-0.1)
        except InvalidInputError:
            caught = caught and True

        self.assertTrue(caught)

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

        caught = False
        try:
            self.my_cube.set_gloss(color=(0.5, 0.5, -0.1, 2.0))
        except InvalidInputError:
            caught = True
        try:
            self.my_cube.set_gloss(rough=-0.1)
        except InvalidInputError:
            caught = caught and True

        self.assertTrue(caught)

    def test_set_mix(self):
        fac = self.my_cube_nodes["Mix Shader"].inputs["Fac"].default_value

        # At this point all values should still be set to their default
        self.assertNotEqual(fac, 0.9)

        # Setting mixer, which will change the values for colour and roughness
        self.my_cube.set_mixer(0.9)
        fac = self.my_cube_nodes["Mix Shader"].inputs["Fac"].default_value

        # Now the values should be changed to that which we have set them to
        self.assertAlmostEqual(fac, 0.9)

        caught = False
        try:
            self.my_cube.set_mixer(1.1)
        except InvalidInputError:
            caught = True
        try:
            self.my_cube.set_mixer(-0.1)
        except InvalidInputError:
            caught = caught and True

        self.assertTrue(caught)

    def test_set_mesh_bbvol(self):
        my_cube = bpy.data.objects['Cube']

        self.my_cube.set_mesh_bbvol(1.0)

        self.assertAlmostEqual(my_cube.scale[0], 0.5)
        self.assertAlmostEqual(my_cube.scale[1], 0.5)
        self.assertAlmostEqual(my_cube.scale[2], 0.5)

        self.my_cube.set_mesh_bbvol(9.3)

        self.assertAlmostEqual(my_cube.scale[0], math.pow(9.3/8.0, 1./3.))
        self.assertAlmostEqual(my_cube.scale[1], math.pow(9.3/8.0, 1./3.))
        self.assertAlmostEqual(my_cube.scale[2], math.pow(9.3/8.0, 1./3.))

        caught = False
        try:
            self.my_cube.set_mesh_bbvol(-1.0)
        except InvalidInputError:
            caught = True

        self.assertTrue(caught)


if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
