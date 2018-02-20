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
    def test_cube_creation(self):
        # To pass the test these two conditions must be satisfied
        # I.e. Cube.001 must not be present before, and must be present after
        no_cube_before = False
        cube_after = False

        # Check if cube is present before
        for obj in bpy.data.objects:
            if obj.name == "Cube.001":
                break
        else:
            no_cube_before = True

        # Create cube
        my_cube = BlenderCube()

        # Check if cube is present after
        for obj in bpy.data.objects:
            if obj.name == "Cube.001":
                cube_after = True
                break

        self.assertTrue(no_cube_before, "There was already a Cube.001 before a cube was created!")
        self.assertTrue(cube_after, "There was no Cube.001 even though it was supposed to have been created!")

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


# For reference in case it is needed
#
# def main():
#     my_cube = BlenderCube()
#     my_cube.set_diffuse();
#     my_cube.set_gloss();
#     print(my_cube.nodes['node_diff'])
#     print(my_cube.nodes['node_gloss'])
#     print(my_cube)
#     check = bpy.context.selected_objects[0]
#     print(check)
#     print(bpy.data.objects)
#     # print all objects
#     for obj in bpy.data.objects:
#         print(obj.name)
#     # my_scene = BlenderScene(bpy.data)
#     # print(my_cube.nodes['node_diff'])
#     # print("print(my_cube.node_tree)")
#     # print(my_cube.node_tree)
#     # print("print(bpy.data.objects['Cube.001'].data.materials[0].node_tree)")
#     # print(bpy.data.objects['Cube.001'].data.materials[0].node_tree.nodes['node_gloss'])
#         # print(key)
#         # print(value)
#     print(bpy.data.objects['Cube.001'].data.materials[0].node_tree.nodes)
#     print(bpy.data.objects['Cube.001'].data.materials[0].node_tree.nodes["Glossy BSDF"].inputs)
#
#     for i in bpy.data.objects['Cube.001'].data.materials[0].node_tree.nodes["Glossy BSDF"].inputs:
#         print(i)
#
#     for i in bpy.data.objects['Cube.001'].data.materials[0].node_tree.nodes["Glossy BSDF"].inputs["Color"].default_value:
#         print(i)
#
#
#     # print(bpy.data.objects['Cube.001'].data)
#
#
#
# main()
