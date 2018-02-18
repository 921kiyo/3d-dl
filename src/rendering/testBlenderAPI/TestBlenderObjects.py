import bpy
import sys
import mathutils as mathU

boop = 'D:/PycharmProjects/Lobster/src/'
ext = 'D:/Anaconda3/envs/tensorflow/Lib/site-packages/'
if not (boop in sys.path):
    sys.path.append(boop)
if not (ext in sys.path):
    sys.path.append(ext)

import rendering.BlenderAPI.BlenderObjects as bld

import unittest
import coverage

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
        obj.set_location(2.0,2.5,-1.0)
        self.assertEqual(obj.reference.location, mathU.Vector((2.0,2.5,-1.0)))

    def test_set_rotation(self):
        obj = bld.BlenderTestObject()
        # set rotation to 45.0, then rotates back 45.0
        obj.set_rot(45.0, 2, 1, 3)
        q = bld.to_quaternion(45.0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)
        obj.rotate(-45.0, 2, 1, 3)
        q = bld.to_quaternion(0, 2, 1, 3)
        self.assertEqual(obj.reference.rotation_quaternion, q)

    def test_set_scale(self):
        # set scale
        obj = bld.BlenderTestObject()
        obj.set_scale((2.0,2.0,2.0))
        self.assertEqual(obj.reference.scale, mathU.Vector((2.0,2.0,2.0)))
        obj.set_scale((-2.0, -2.0, -2.0))
        self.assertEqual(obj.reference.scale , mathU.Vector((-2.0, -2.0, -2.0)))

    def test_delete(self):
        obj = bld.BlenderTestObject()
        obj.delete()
        num_objects_after = len(bpy.data.objects)
        self.assertEqual(num_objects_after, 0)

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
    cov.stop()
    cov.save()
    cov.html_report()

