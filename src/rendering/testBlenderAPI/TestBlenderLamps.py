import bpy
import sys
import mathutils as mathU

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld

import unittest

class BlenderLampsTest(unittest.TestCase):

    def setUp(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()


    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()


    def test_create_blenderpoint_no_reference(self):
        num_objects_before = len(bpy.data.objects)

        lamp1 = bld.BlenderPoint(None)
        lamp2 = bld.BlenderPoint(None)
        lamp3 = bld.BlenderPoint(None)

        num_objects_after = len(bpy.data.objects)

        self.assertGreater(num_objects_after, num_objects_before, 'Number of objects did not increase!')

    def test_create_lamp_reference(self):
        # add objects manually
        # if feed API
        """
        1. put right ob in blender
        2.

        """
        bpy.ops.object.add()
        obj_reference = bpy.data.objects[0]

        # create object with reference
        num_objects_before = len(bpy.data.objects)
        obj = bld.BlenderLamp(obj_reference)

        num_objects_after = len(bpy.data.objects)

        self.assertEqual(num_objects_after, num_objects_before, 'Number of objects changed!')
        self.assertEqual(obj.reference, obj_reference)
        self.assertTrue('Empty' in bpy.data.objects.keys())
    #     when blender creates an ob, key of ob is name of type o fob.



    def test_delete_lamp(self):
        # add objects manually
        bpy.ops.object.add()
        obj_reference = bpy.data.objects[0]

        num_objects_before = len(bpy.data.objects)

        lamp = bld.BlenderLamp(obj_reference)
        lamp.delete()

        num_objects_after = len(bpy.data.objects)

        self.assertLess(num_objects_after, num_objects_before)

    def test_create_operation(self):
        pass
        # Note clear exactly what this is meant to do
        # num_objects_before = len(bpy.data.objects)
        #
        # num_objects_after = len(bpy.data.objects)
        #
        # self.assertGreater(num_objects_after, num_objects_before, 'Number of objects did not increase!')


    def test_turn_off(self):
        lamp = bld.BlenderPoint(None)

        lamp.turn_off()

        self.assertEquals(lamp.reference.layers[1], True)
        self.assertEquals(lamp.reference.layers[0], False)

    def test_turn_on(self):
        lamp = bld.BlenderPoint(None)

        lamp.turn_on()

        self.assertEquals(lamp.reference.layers[0], True)
        self.assertEquals(lamp.reference.layers[1], False)

    def test_face_towards(self):
        lamp = bld.BlenderPoint(None)

        # set rotation to 45.0, then rotates back 45.0
        lamp.set_rot(45.0, 2, 1, 3)
        q = bld.to_quaternion(45.0, 2, 1, 3)

        self.assertEqual(lamp.reference.rotation_quaternion, q)

        lamp.rotate(-45.0, 2, 1, 3)
        q = bld.to_quaternion(0, 2, 1, 3)
        self.assertEqual(lamp.reference.rotation_quaternion, q)

    def test_set_size(self):
        lamp = bld.BlenderPoint(None)
        lamp.set_size(100)
        self.assertEquals(lamp.data.shadow_soft_size, 100)


class BlenderSunTest(unittest.TestCase):
    def setUp(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_create_blendersun(self):
        sun = bld.BlenderSun(None)

        self.assertEquals(sun.data.type, 'SUN')

class BlenderAreaTest(unittest.TestCase):
    def setUp(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
    #     check follows multiple changes

    def tearDown(self):
        # create lamp, pass to belnderpoint,
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_create_blenderarea(self):
        sun = bld.BlenderArea(None)
        self.assertEquals(sun.data.type, 'AREA')



if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderLampsTest)
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSunTest))
    success = unittest.TextTestRunner(verbosity=True).run(suite).wasSuccessful()
