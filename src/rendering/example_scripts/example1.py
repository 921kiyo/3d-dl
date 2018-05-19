"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math
import bpy

# IMPORTANT: set render engine as Cycles
bpy.context.scene.render.engine = 'CYCLES'

# path to blender library
boop = 'D:\\PycharmProjects\\Lobster\\src\\rendering\\BlenderAPI'

if not (boop in sys.path):
    sys.path.append(boop)

import src.rendering.BlenderAPI as bld

radius = 10.0

room = bld.BlenderRoom(radius) # add a room ( 6 planes )
# give the existing camera and create an instance of BlenderCamera
cam = bld.BlenderCamera(bpy.data.objects['Camera'])
# give the existing cube and create an instance of BlenderCube
cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
# same for lamp
lamp = bld.BlenderLamp(bpy.data.objects['Lamp'])

# instantiate scene
scene = bld.BlenderScene(bpy.data.scenes[0])
scene.add_object_fixed(room)
scene.add_subject(cube)
scene.add_camera(cam)
scene.add_lamp(lamp)
# load optimal render settings
scene.set_render()

# set camera location to a random point along the shell of a sphere of radius 10.0
x,y,z = bld.random_shell_coords(radius)
cam.set_location((x,y,z))

# set cube location to a random point
x,y,z = bld.random_cartesian_coords(0.0,0.0,0.0,1.0,4.0)
cube.set_location((x,y,z))

# tell camera to face towards the current cube location
cam.face_towards(x,y,z)

# move cube a little more
x,y,z = bld.random_cartesian_coords(x,y,z,0.5,1.0)
cube.set_location((x,y,z))