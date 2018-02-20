import bpy
import sys
import mathutils as mathU

# boop = 'D:/PycharmProjects/Lobster/src/'

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

from rendering.BlenderAPI.BlenderObjects import to_quaternion
import rendering.BlenderAPI as bld

import unittest

class BlenderCameraTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_create_no_reference(self):
        num_objects_before = len(bpy.data.objects)
        obj = bld.BlenderCamera()
        num_objects_after = len(bpy.data.objects)
        self.assertGreater(num_objects_after, num_objects_before, 'Number of objects did not increase!')

        self.assertTrue('Camera' in bpy.data.objects.keys())

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_spin(self):
        cam = bld.BlenderCamera()
        q = cam.get_rot()

        focal_origin = mathU.Vector([0, 0, -1])
        t = q.to_matrix()
        focal_axis = t * focal_origin
        focal_axis.normalize()

        q_rot = to_quaternion(90, *focal_axis)
        q_new = q*q_rot

        cam.spin(90)

        self.assertEqual(q_new, cam.get_rot(), 'Camera spin not correct!')

    def test_face_towards(self):
        # instantiate camera at arbitrary location
        cam = bld.BlenderCamera(location=(2.0,4.0,-1.0))
        # face origin
        cam.face_towards(0.0,0.0,0.0)

        q = cam.get_rot()

        focal_origin = mathU.Vector([0, 0, -1])
        t = q.to_matrix()
        focal_axis = t * focal_origin
        focal_axis.normalize()

        cam_loc_norm = cam.reference.location
        cam_loc_norm.normalize()

        # camera location should be parallel to vector of focal axis
        self.assertAlmostEqual(cam_loc_norm[0], -focal_axis[0], places=5)
        self.assertAlmostEqual(cam_loc_norm[1], -focal_axis[1], places=5)
        self.assertAlmostEqual(cam_loc_norm[2], -focal_axis[2], places=5)

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderCameraTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
