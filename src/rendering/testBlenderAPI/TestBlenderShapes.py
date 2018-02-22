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

class BlenderShapeTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()


    def test_cube_creation(self):
        # To pass the test these two conditions must be satisfied
        # I.e. Cube must not be present before, and must be present after
        no_cube_before = False
        cube_after = False

        # Check if cube is present before
        for obj in bpy.data.objects:
            if obj.name == "Cube":
                break
        else:
            no_cube_before = True

        # Create cube
        my_cube = BlenderCube()

        # Check if cube is present after
        for obj in bpy.data.objects:
            if obj.name == "Cube":
                cube_after = True
                break

        self.assertTrue(no_cube_before, "There was already a Cube before a cube was created!")
        self.assertTrue(cube_after, "There was no Cube even though it was supposed to have been created!")

    def test_plane_creation(self):
        # To pass the test these two conditions must be satisfied
        # I.e. Plane must not be present before, and must be present after
        no_plane_before = False
        plane_after = False

        # Check if plane is present before
        for obj in bpy.data.objects:
            if obj.name == "Plane":
                break
        else:
            no_plane_before = True

        # Create cube
        my_plane = BlenderPlane()

        # Check if cube is present after
        for obj in bpy.data.objects:
            if obj.name == "Plane":
                plane_after = True
                break

        self.assertTrue(no_plane_before, "There was already a Plane before a plane was created!")
        self.assertTrue(plane_after, "There was no Plane even though it was supposed to have been created!")


if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()

