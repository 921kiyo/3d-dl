"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math

boop = 'D:/PycharmProjects/Lobster/src/rendering'

if not (boop in sys.path):
	sys.path.append(boop)

import BlenderObjects as bo

radius = 10.0

room = bo.BlenderRoom(radius)
room.assign_random_colors()
cam = bo.BlenderCamera(bpy.data.objects['Camera'])
cube = bo.BlenderCube(reference=bpy.data.objects['Cube'])
lamp = bo.BlenderLamp(bpy.data.objects['Lamp'],bpy.data.lamps[0])

# instantiate scene
scene = bo.BlenderScene(bpy.data.scenes[0])
scene.add_object_fixed(room)
scene.add_subject(cube)
scene.add_camera(cam)
scene.add_lamp(lamp)
scene.set_render()

x,y,z = bo.random_shell_coords(radius)

cam.set_location((x,y,z))

x,y,z = bo.random_cartesian_coords(0.0,0.0,0.0,1.0,4.0)

cube.set_location((x,y,z))

cam.face_towards(x,y,z)

x,y,z = bo.random_cartesian_coords(x,y,z,0.5,1.0)

cube.set_location((x,y,z))