import bpy
import sys
import mathutils as mathU

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI.BlenderObjects as bld
from rendering.BlenderAPI.BlenderExceptions import *

import unittest


class BlenderObjectTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_create_no_reference(self):
        num_objects_before = len(bpy.data.objects)
        obj = bld.BlenderTestObject()
        num_objects_after = len(bpy.data.objects)
        self.assertGreater(num_objects_after, num_objects_before, 'Number of objects did not increase!')

        self.assertTrue( 'Empty' in bpy.data.objects.keys())

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_create_with_reference(self):
        # add objects manually
        bpy.ops.object.add()
        obj_reference = bpy.data.objects[0]

        # create object with reference
        num_objects_before = len(bpy.data.objects)
        obj = bld.BlenderTestObject(reference = obj_reference)
        num_objects_after = len(bpy.data.objects)
        self.assertEqual(num_objects_after, num_objects_before, 'Number of objects changed!')
        self.assertEqual(obj.reference, obj_reference)
        self.assertTrue('Empty' in bpy.data.objects.keys())

    def test_set_location(self):

        # set random location
        obj = bld.BlenderTestObject()
        
        # all positive
        obj.set_location(2.0,2.5,1.0)
        self.assertEqual(obj.reference.location, mathU.Vector((2.0,2.5,1.0)))
        
        # mixed
        obj.set_location(2.0,2.5,-1.0)
        self.assertEqual(obj.reference.location, mathU.Vector((2.0,2.5,-1.0)))
        
        # all negative
        obj.set_location(-2.0,-2.5,-1.0)
        self.assertEqual(obj.reference.location, mathU.Vector((-2.0,-2.5,-1.0)))

    def test_set_invlid_location(self):

        caught = False
        try:
            obj = bld.BlenderTestObject(location=(0,0))
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)


    def test_set_rotation(self):
        
        obj = bld.BlenderTestObject()
        
        # zero rotation
        obj.set_rot(0.0, 2, 1, 3)
        q = bld.to_quaternion(0.0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)
        # zero vector
        obj.set_rot(0.0, 0, 0, 0)
        q = bld.to_quaternion(0.0, 0, 0, 0)
        self.assertEqual(obj.reference.rotation_quaternion, q)

        # set rotation to 45.0, then rotates back -45.0
        obj.set_rot(45.0, 2, 1, 3)
        q = bld.to_quaternion(45.0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)
        obj.rotate(-45.0, 2, 1, 3)
        q = bld.to_quaternion(0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)

        # set rotation to -45.0, then rotates back 45.0
        obj.set_rot(-45.0, 2, 1, 3)
        q = bld.to_quaternion(-45.0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)
        obj.rotate(45.0, 2, 1, 3)
        q = bld.to_quaternion(0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)

    def test_set_scale(self):
        # set scale
        obj = bld.BlenderTestObject()
        obj.set_scale((2.0,2.0,2.0))
        self.assertEqual(obj.reference.scale, mathU.Vector((2.0,2.0,2.0)))
        caught = False
        try:
            obj.set_scale((-2.0, -2.0, -2.0))
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

    def test_delete(self):
        # delete the first time
        obj = bld.BlenderTestObject()
        obj.delete()
        num_objects_after = len(bpy.data.objects)
        self.assertEqual(num_objects_after, 0)

        # delete the second time
        obj.delete()

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
