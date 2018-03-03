import bpy
import sys
import unittest

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld
from rendering.BlenderAPI.BlenderExceptions import *


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
        """
        1. put right ob in blender
        2.

        """
        bpy.ops.object.add()
        obj_reference = bpy.data.objects[0]

        num_objects_before = len(bpy.data.objects)

        obj = bld.BlenderTestLamp(obj_reference)

        num_objects_after = len(bpy.data.objects)

        self.assertEqual(num_objects_after, num_objects_before, 'Number of objects changed!')
        self.assertEqual(obj.reference, obj_reference)

        # when blender creates an object, the key of object is its type
        self.assertTrue('Empty' in bpy.data.objects.keys())

    def test_delete_lamp(self):
        bpy.ops.object.lamp_add(type='POINT')
        obj_reference = bpy.data.objects[0]

        num_objects_before = len(bpy.data.objects)

        lamp = bld.BlenderTestLamp(obj_reference)
        lamp.delete()

        num_objects_after = len(bpy.data.objects)

        self.assertLess(num_objects_after, num_objects_before)

    def test_turn_off(self):
        bpy.ops.object.lamp_add(type='POINT')
        lamp_reference = bpy.data.objects[0]

        lamp = bld.BlenderTestLamp(lamp_reference)
        lamp.turn_off()

        self.assertEquals(lamp_reference.layers[1], True)
        self.assertEquals(lamp_reference.layers[0], False)

    def test_turn_on(self):
        bpy.ops.object.lamp_add(type='POINT')
        lamp_reference = bpy.data.objects[0]

        lamp = bld.BlenderTestLamp(lamp_reference)
        lamp.turn_on()

        self.assertEquals(lamp_reference.layers[0], True)
        self.assertEquals(lamp_reference.layers[1], False)

    def test_face_towards(self):
        # instantiate camera at arbitrary location
        lamp = bld.BlenderTestLamp(location=(2.0,4.0,-1.0))
        lamp_reference = bpy.data.objects['Point']
        # face origin
        lamp.face_towards(0.0,0.0,0.0)

        q = lamp.get_rot()

        focal_origin = mathU.Vector([0, 0, -1])
        t = q.to_matrix()
        focal_axis = t * focal_origin
        focal_axis.normalize()

        lamp_loc_norm = lamp.reference.location
        lamp_loc_norm.normalize()

        # camera location should be parallel to vector of focal axis
        self.assertAlmostEqual(lamp_loc_norm[0], -focal_axis[0], places=5)
        self.assertAlmostEqual(lamp_loc_norm[1], -focal_axis[1], places=5)
        self.assertAlmostEqual(lamp_loc_norm[2], -focal_axis[2], places=5)

        # face random
        lamp.face_towards(20.0, -10.0, 0.0)

        q = lamp.get_rot()

        focal_origin = mathU.Vector([0, 0, -1])
        t = q.to_matrix()
        focal_axis = t * focal_origin
        focal_axis.normalize()

        lamp_loc_norm = lamp.reference.location - mathU.Vector((20.0, -10.0, 0.0))
        lamp_loc_norm.normalize()

        # camera location should be parallel to vector of focal axis
        self.assertAlmostEqual(lamp_loc_norm[0], -focal_axis[0], places=5)
        self.assertAlmostEqual(lamp_loc_norm[1], -focal_axis[1], places=5)
        self.assertAlmostEqual(lamp_loc_norm[2], -focal_axis[2], places=5)


    def test_set_brightness(self):
        bpy.ops.object.lamp_add(type='POINT')
        lamp_reference = bpy.data.objects[0]
        lamp = bld.BlenderTestLamp(lamp_reference)

        lamp.set_brightness(100)
        strength_node = lamp_reference.data.node_tree.nodes["Emission"]
        self.assertEquals(strength_node.inputs["Strength"].default_value, 100)
        lamp.set_brightness(0.5)
        self.assertEquals(strength_node.inputs["Strength"].default_value, 0.5)

        caught = False
        try:
            lamp.set_brightness(-10)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

    def test_set_size(self):
        bpy.ops.object.lamp_add(type='POINT')
        lamp_reference = bpy.data.objects[0]
        lamp = bld.BlenderTestLamp(lamp_reference)

        lamp.set_size(100)
        self.assertEquals(lamp_reference.data.shadow_soft_size, 100)
        lamp.set_size(0.5)
        self.assertEquals(lamp_reference.data.shadow_soft_size, 0.5)

        caught = False
        try:
            lamp.set_size(-10)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

    def test_create_blendersun(self):
        sun = bld.BlenderSun(None)
        self.assertEquals(sun.data.type, 'SUN')

    def test_create_blenderarea(self):
        area = bld.BlenderArea(None)
        self.assertEquals(area.data.type, 'AREA')

    def test_create_blenderpoint(self):
        point = bld.BlenderPoint(None)
        self.assertEquals(point.data.type, 'POINT')



if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderLampsTest)
    success = unittest.TextTestRunner(verbosity=True).run(suite).wasSuccessful()
