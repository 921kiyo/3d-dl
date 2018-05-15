import bpy

import sys
from copy import copy

boop = '/Users/matthew/Documents/MSc/Group_Project/Lobster/src/'
if not (boop in sys.path):
    sys.path.append(boop)

C = bpy.context
C.scene.render.engine = 'CYCLES'


import unittest


import rendering.BlenderAPI as bld


from rendering.BlenderAPI.BlenderScene import BlenderScene, BlenderRandomScene
from rendering.BlenderAPI.BlenderScene import BlenderRoom
from rendering.BlenderAPI.BlenderCamera import BlenderCamera
from rendering.BlenderAPI.BlenderLamps import BlenderLamp, BlenderSun, BlenderPoint

import os

class BlenderSceneTest(unittest.TestCase):


    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        self.my_scene = BlenderScene(bpy.data.scenes[0])

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_room_has_correct_number_of_walls(self):
        self.my_room = BlenderRoom(10)
        number_of_walls = len(self.my_room.walls)
        self.assertEqual(number_of_walls, 6, "Room does not have 6 walls!")

    def test_room_deletes_properly(self):
        self.my_room = BlenderRoom(10)
        self.my_room.delete()
        walls_post_deletion = self.my_room.walls
        self.assertEqual(walls_post_deletion, [], "Walls were not deleted properly!")

    def test_scene_is_set_up_correctly(self):
        self.assertEqual(self.my_scene.lamps, [])
        self.assertEqual(self.my_scene.background, None)
        self.assertEqual(self.my_scene.objects_fixed, [])
        self.assertEqual(self.my_scene.objects_unfixed, [])
        self.assertEqual(self.my_scene.camera, None)
        self.assertEqual(self.my_scene.subject, None)
        self.assertEqual(self.my_scene.data, bpy.data.scenes[0])

    def test_add_camera(self):
        new_camera = BlenderCamera()
        self.my_scene.add_camera(new_camera)
        self.assertEqual(self.my_scene.camera, new_camera, "Camera was not successfully added to scene!")

    def test_add_lamps(self):
        # Add one lamp and check that it is successfully added
        new_lamp_sun = BlenderSun()
        self.my_scene.add_lamp(new_lamp_sun)
        self.assertEqual(self.my_scene.lamps[0], new_lamp_sun, "Lamp (sun) was not successfully added to scene!")
        # Add another lamp of a different type and check that it is successfully added; also verify that previous lamp is still in position
        new_lamp_point = BlenderPoint()
        self.my_scene.add_lamp(new_lamp_point)
        self.assertEqual(self.my_scene.lamps[0], new_lamp_sun, "Lamp (sun) was not retained when new lamp was added to scene!")
        self.assertEqual(self.my_scene.lamps[1], new_lamp_point, "Lamp (point) was not successfully added to scene!")


    # Currently failing test because delete assumes that everything would have been instantiated first
    def test_delete_all(self):
        self.my_scene.delete_all();
        # Everything should now be back to its original state
        self.assertEqual(self.my_scene.lamps, [])
        self.assertEqual(self.my_scene.background, None)
        self.assertEqual(self.my_scene.objects_fixed, [])
        self.assertEqual(self.my_scene.objects_unfixed, [])
        self.assertEqual(self.my_scene.camera, None)
        self.assertEqual(self.my_scene.subject, None)
        self.assertEqual(self.my_scene.data, bpy.data.scenes[0])
        self.assertEqual(len(bpy.data.objects.keys()), 0) # TODO fix this!

    def test_add_subject(self):
        new_subject_cube = bld.BlenderCube()
        self.my_scene.add_subject(new_subject_cube)
        self.assertEqual(self.my_scene.subject, new_subject_cube, "Subject (cube) was not successfully added to scene!")
        self.my_scene.delete_all();

    def test_add_object_fixed(self):
        new_room = BlenderRoom(10)
        self.my_scene.add_object_fixed(new_room)
        # Check that room was successfully added
        self.assertTrue(self.my_scene.objects_fixed[0] == new_room, "Fixed object (room) was not successfully added to scene!")
        # Check that one and only one object was added
        self.assertEqual(len(self.my_scene.objects_fixed), 1, "Incorrect number of elements in objects_fixed list")
        self.my_scene.delete_all();

    def test_add_object_unfixed(self):
        new_object_cube = bld.BlenderCube()
        self.my_scene.add_object_unfixed(new_object_cube)
        # Check that the cube was successfully added
        self.assertEqual(self.my_scene.objects_unfixed[0], new_object_cube, "Subject (cube) was not successfully added to scene!")
        # Check that one and only one object was added
        self.assertEqual(len(self.my_scene.objects_unfixed), 1, "Incorrect number of elements in objects_fixed list")
        self.my_scene.delete_all();

    def test_render_creation(self):
        self.my_scene.set_render()
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        filepath = os.path.join(os.path.dirname(__file__), 'test_files' , 'render_test_1.png')
        self.my_scene.render_to_file(filepath)
        self.assertTrue(os.path.isfile(filepath))
        os.remove(filepath)

class BlenderRandomSceneTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        self.my_scene = BlenderRandomScene(bpy.data.scenes[0])

    def tearDown(self):
        # delete all objects
        self.my_scene.delete_all()
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def testImportSingleSubject(self):
        # delete all the extra stuff added by BlenderRandomScene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        # add the object
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)
        self.assertEqual(len(bpy.data.objects), 1, 'Not one object added!')
        self.assertEqual(bpy.data.objects[0], self.my_scene.subject.reference, 'subject and object reference not equal!')

    def testImportTwoSubjects(self):
        # delete all the extra stuff added by BlenderRandomScene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        # add the object
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        obj_path_bot = obj_path
        texture_path_bot = texture_path
        self.my_scene.load_subject_from_path(obj_path, texture_path, obj_path_bot, texture_path_bot)
        self.assertEqual(len(bpy.data.objects), 2, 'Not two objects added!')
        self.assertEqual(bpy.data.objects[0], self.my_scene.subject.reference, 'subject and object reference not equal!')
        self.assertEqual(bpy.data.objects[1], self.my_scene.subject_bot.reference, 'subject and object reference not equal!')

    def test_camera_loc(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        camera_locations = []
        N = 1000
        for i in range(N):
            self.my_scene.scene_setup()
            camera_locations.append(copy(tuple(self.my_scene.camera.reference.location)))

        logs = self.my_scene.retrieve_logs()
        loc = logs["camera_loc"]
        rad = logs["camera_radius"]
        for i in range(N):
            left = loc[i]
            right = camera_locations[i]
            (x,y,z) = (left[0]*rad[i], left[1]*rad[i], left[2]*rad[i])
            left = (x,y,z)
            for l,r in zip(left,right):
                self.assertAlmostEqual(l, r, places=5)

    def test_render_creation(self):
        # note CUDA device is not set here, so this might take a bit long
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)
        
        for i in range(5):
            filepath = os.path.join(os.path.dirname(__file__), 'test_files' , 'render_test_1.png')
            self.my_scene.render_to_file(filepath)
            self.assertTrue(os.path.isfile(filepath))
            os.remove(filepath)

    def test_lamp_loc(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        lamp_locations = []
        N = 1000
        for i in range(N):
            self.my_scene.scene_setup()
            for lamp in self.my_scene.lamps:
                if not lamp.is_on() is True:
                    continue
                lamp_locations.append(copy(tuple(lamp.reference.location)))
                
        logs = self.my_scene.retrieve_logs()
        loc = logs["lamp_loc"]
        rad = logs["lamp_distance"]
        for i in range(len(loc)):
            left = loc[i]
            right = lamp_locations[i]
            (x,y,z) = (left[0]*rad[i], left[1]*rad[i], left[2]*rad[i])
            left = (x,y,z)
            for l,r in zip(left,right):
                self.assertAlmostEqual(l, r, places=5)

    def test_lamp_num(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files', 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files', 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        lamp_locations = []

        # vary the max number of lamps
        self.my_scene.set_attribute_distribution_params('num_lamps', 'mid', 5)
        self.my_scene.set_attribute_distribution_params('num_lamps', 'scale', 0)
        self.my_scene.scene_setup()
        self.assertEqual(5, self.my_scene.max_num_lamps, "Number of lamps not correct")
        self.assertEqual(5, len(self.my_scene.lamps), "Number of lamps not correct")
        self.my_scene.set_attribute_distribution_params('num_lamps', 'mid', 7)
        self.my_scene.set_attribute_distribution_params('num_lamps', 'scale', 0)
        self.my_scene.scene_setup()
        self.assertEqual(7, self.my_scene.max_num_lamps, "Number of lamps not correct")
        self.assertEqual(7, len(self.my_scene.lamps), "Number of lamps not correct")

        self.my_scene.clear_logs()
        # test the number of turned on lamps
        N =50
        counts = []
        for i in range(N):
            self.my_scene.scene_setup() # sampling takes place here
            # count the number of lamps that's turned on
            count = 0
            for lamp in self.my_scene.lamps:
                if lamp.is_on():
                    count += 1
            counts.append(count)
        logs = self.my_scene.retrieve_logs()
        num_recorded = logs["num_lamps"]
        self.assertEqual(counts, num_recorded)

    def test_bad_dist_lamp(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        self.assertRaises(ValueError, self.my_scene.set_attribute_distribution_params,
                          'lamp_distance', 'sigmu', -2)
        self.my_scene.set_attribute_distribution_params('lamp_distance', 'l', -1)
        self.assertRaises(ValueError,self.my_scene.set_attribute_distribution_params('lamp_distance', 'r', -3))
        
        self.assertRaises(ValueError, self.my_scene.scene_setup)
        

    def test_bad_dist_cam(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        self.assertRaises(ValueError, self.my_scene.set_attribute_distribution_params,
                          'camera_radius', 'sigmu', -2)
        self.my_scene.set_attribute_distribution_params('camera_radius', 'l', -1)
        self.assertRaises(ValueError, self.my_scene.set_attribute_distribution_params('camera_radius', 'r', -3))
        
        self.assertRaises(ValueError, self.my_scene.scene_setup)

    def test_bad_dist_numlamp(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # add a subject
        obj_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'example.obj')
        texture_path = os.path.join(os.path.dirname(__file__), 'test_files' , 'texture.jpg')
        self.my_scene.load_subject_from_path(obj_path, texture_path)

        self.assertRaises(ValueError, self.my_scene.set_attribute_distribution_params,'num_lamps', 'mid', -25)
        self.assertRaises(ValueError, self.my_scene.set_attribute_distribution_params,'num_lamps', 'mid', -0.5)

    def test_set_distribution_params(self):
        # test that the camera location corresponds to the location reported in logs
        camera = bld.BlenderCamera()
        bpy.context.scene.camera = camera.reference
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.my_scene.set_render()
        self.my_scene.add_camera(cam)

        # Number of Lamps - Uniform Discrete
        self.my_scene.set_attribute_distribution_params('num_lamps', 'mid', 25)
        self.my_scene.set_attribute_distribution_params('num_lamps', 'scale', 0.2)

        self.assertEquals(self.my_scene.num_lamps.l, 20)
        self.assertEquals(self.my_scene.give_params()['num_lamps']['mid'], 25)
        self.assertEquals(self.my_scene.num_lamps.r, 30)
        self.assertEquals(self.my_scene.give_params()['num_lamps']['scale'], 0.2)

        self.my_scene.set_attribute_distribution_params('num_lamps', 'mid', 2)
        self.my_scene.set_attribute_distribution_params('num_lamps', 'scale', 0.5)

        self.assertEquals(self.my_scene.num_lamps.l, 1)
        self.assertEquals(self.my_scene.give_params()['num_lamps']['mid'], 2)
        self.assertEquals(self.my_scene.num_lamps.r, 3)
        self.assertEquals(self.my_scene.give_params()['num_lamps']['scale'], 0.5)

        # Lamp Energy - Truncated Normal
        self.my_scene.set_attribute_distribution_params('lamp_energy', 'mu', 2000.0)
        self.my_scene.set_attribute_distribution_params('lamp_energy', 'sigmu', 0.5)

        self.assertAlmostEquals(self.my_scene.lamp_energy.mu, 2000.0)
        self.assertAlmostEquals(self.my_scene.give_params()['lamp_energy']['mu'], 2000.0)
        self.assertAlmostEquals(self.my_scene.lamp_energy.sigmu, 0.5)
        self.assertAlmostEquals(self.my_scene.give_params()['lamp_energy']['sigmu'], 0.5)

        self.my_scene.set_attribute_distribution_params('lamp_energy', 'mu', 300.0)
        self.my_scene.set_attribute_distribution_params('lamp_energy', 'sigmu', 2.0)

        self.assertAlmostEquals(self.my_scene.lamp_energy.mu, 300.0)
        self.assertAlmostEquals(self.my_scene.give_params()['lamp_energy']['mu'], 300.0)
        self.assertAlmostEquals(self.my_scene.lamp_energy.sigmu, 2.0)
        self.assertAlmostEquals(self.my_scene.give_params()['lamp_energy']['sigmu'], 2.0)

        # Camera Location - CompositeShellRing
        self.my_scene.set_attribute_distribution_params('camera_loc', 'phi_sigma', 6.6)
        self.my_scene.set_attribute_distribution_params('camera_loc', 'normals', 'X')

        self.assertAlmostEquals(self.my_scene.camera_loc.phi_sigma, 6.6)
        self.assertAlmostEquals(self.my_scene.give_params()['camera_loc']['phi_sigma'], 6.6)
        self.assertEquals(self.my_scene.camera_loc.normals, 'X')
        self.assertEquals(self.my_scene.give_params()['camera_loc']['normals'], 'X')

        self.my_scene.set_attribute_distribution_params('camera_loc', 'phi_sigma', 0.0)
        self.my_scene.set_attribute_distribution_params('camera_loc', 'normals', 'XZ')

        self.assertAlmostEquals(self.my_scene.camera_loc.phi_sigma, 0.0)
        self.assertAlmostEquals(self.my_scene.give_params()['camera_loc']['phi_sigma'], 0.0)
        self.assertEquals(self.my_scene.camera_loc.normals, 'XZ')
        self.assertEquals(self.my_scene.give_params()['camera_loc']['normals'], 'XZ')
        
                
if __name__ == '__main__':
    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSceneTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderRandomSceneTest))
    alltests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(alltests).wasSuccessful()
