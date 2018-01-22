"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math
import mathutils
import bpy
import csv

bpy.context.scene.render.engine = 'CYCLES'

boop = 'D:/PycharmProjects/Lobster/src/rendering'

if not (boop in sys.path):
	sys.path.append(boop)

import BlenderObjects as bo

def list_distances(L1,L2):
	V = mathutils.Vector(L1) - mathutils.Vector(L2)
	return V.magnitude

# delete the initial cube
cube = bo.BlenderCube(reference=bpy.data.objects['Cube'])
cube.delete()
	
# import product obj file and instantiate object
obj_path = 'D:\\PycharmProjects\\Lobster\\src\\rendering\\9562dwzzz4sg-BottleBeerCorona\\Corona\\Corona.obj'
status = bpy.ops.import_scene.obj(filepath=obj_path)
product = bpy.context.selected_objects[0]
	
product = bo.BlenderCube(reference=product, location=(-1,0,-1) ,orientation=(0,0,1,0))
product.add_image_texture('D:\\PycharmProjects\\Lobster\\src\\rendering\\9562dwzzz4sg-BottleBeerCorona\\Corona\\BotellaText.jpg')
product.set_diffuse(color=(1,0,0,1),rough=0.1)
product.set_gloss(rough=0.1)
product.set_mixer(0.6)
product.set_scale((.1,.1,.1))
product.toggle_smooth()

# Create a cube
cube2 = bo.BlenderCube(location = (3,3,3))
cube2.set_scale((.5,.5,.5))
cube2.set_diffuse(color=(0,0,1,1),rough=0.1)
cube2.set_gloss(rough=0.1)
cube2.set_mixer(0.3)

# Fetch the camera and lamp
cam = bo.BlenderCamera(bpy.data.objects['Camera'])
lamp = bo.BlenderLamp(bpy.data.objects['Lamp'])

# Create a 2nd lamp
lamp2 = bo.BlenderLamp(None)
lamp.set_brightness(500.00)
lamp.set_size(5.0)
lamp2.set_brightness(500.00)
lamp2.set_size(5.0)

# instantiate scene
scene = bo.BlenderScene(bpy.data.scenes[0])
scene.set_render()
with open('D:\\PycharmProjects\\Lobster\\src\\rendering\\9562dwzzz4sg-BottleBeerCorona\\Corona\\render\\camera.csv','w') as csvfile:
	coord_writer = csv.writer(csvfile, delimiter=',')
	for i in range(1000):
	
		x,y,z = bo.random_shell_coords(5.0)
		lamp.set_location((x,y,z))

		x,y,z = bo.random_shell_coords(5.0)
		lamp2.set_location((x,y,z))

		scene.add_object_unfixed(product)
		scene.add_object_unfixed(cube2)

		x,y,z = bo.random_shell_coords(7.0)
		cam.set_location((x,y,z))
		cam.face_towards(0.0,0.0,0.0)

		loc = bo.random_cartesian_coords(0.0,0.0,0.0,1.0,4.0)
		product.set_location((loc))
		
		is_flip = (random.uniform(0,1)<0.5)
		if is_flip:
			product.set_rot(90,0,1,0)
			coord_writer.writerow([x,y,z])
		else:
			product.set_rot(0,0,1,0)
			coord_writer.writerow([x,-z,y])	
		
		loc2 = loc

		while(list_distances(loc, loc2) < math.sqrt(3)):
			loc2 = bo.random_cartesian_coords(0.0,0.0,0.0,3.0,4.0)

		cube2.set_location(loc2)
		scene.render_to_file('D:\\PycharmProjects\\Lobster\\src\\rendering\\9562dwzzz4sg-BottleBeerCorona\\Corona\\render\\render%d.png'%i)