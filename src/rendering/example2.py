"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math
import mathutils
import bpy
import csv
import os

# set use GPU
C = bpy.context
C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
C.user_preferences.addons['cycles'].preferences.devices[0].use = True
C.scene.render.engine = 'CYCLES'

# path to blender library
boop = 'D:\\PycharmProjects\\Lobster\\src\\rendering\\BlenderAPI'


if not (boop in sys.path):
    sys.path.append(boop)


import BlenderAPI as bld


def list_distances(L1,L2):
    V = mathutils.Vector(L1) - mathutils.Vector(L2)
    return V


# delete the initial cube
cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
cube.delete()

""" ************* User specified stuff here ************* """
# Specify number of images to render
num_images = 10
# required file paths for the script to run
obj_path = 'D:\\PycharmProjects\\Product3\\Rubicon\\Rubicon.obj'
texture_path = 'D:\\PycharmProjects\\Product3\\Rubicon\\Rubicon.jpg'
render_folder = 'D:\\PycharmProjects\\Product3\\Rubicon\\render'
csv_path = os.path.join(render_folder,'camera.csv')

# Import the shape, and give texture image
product = bld.BlenderImportedShape(obj_path=obj_path, location=(-1,0,-1) ,orientation=(0,0,1,0))
product.add_image_texture(texture_path)
product.set_diffuse(color=(1,0,0,1),rough=0.1)
product.set_gloss(rough=0.1)
product.set_mixer(0.3)
product.set_scale((1,1,1))
product.toggle_smooth()

# Create a cube
cube2 = bld.BlenderCube(location = (3,3,3))
cube2.set_scale((.5,.5,.5))
cube2.set_diffuse(color=(0,0,1,1),rough=0.1)
cube2.set_gloss(rough=0.1)
cube2.set_mixer(0.3)

# Fetch the camera and lamp
cam = bld.BlenderCamera(bpy.data.objects['Camera'])
lamp = bld.BlenderPoint(bpy.data.objects['Lamp'])

# Create a 2nd lamp
lamp2 = bld.BlenderPoint(None)

# instantiate scene
scene = bld.BlenderScene(bpy.data.scenes[0])
scene.set_render()

with open(csv_path,'w') as csvfile:

    coord_writer = csv.writer(csvfile, delimiter=',')

    for i in range(num_images):

        is_flip = (random.uniform(0,1)<0.5)

        # random locations of lamps along shell coordinates
        x,y,z = bld.random_shell_coords(5.0)
        lamp.set_location((x,y,z))
        x,y,z = bld.random_shell_coords(5.0)
        lamp2.set_location((x,y,z))

        # random location of camera along shell coordinates
        x,y,z = bld.random_shell_coords(7.0)
        cam.set_location((x,y,z))
        # face towards the centre
        cam.face_towards(0.0,0.0,0.0)

        # randomize spin of camera
        spin_angle = random.uniform(0.0,360.0)
        cam.spin(spin_angle)

        loc = bld.random_cartesian_coords(0.0,0.0,0.0,1.0,4.0)
        product.set_location((loc))

        # flip subject 90 degrees along one axis, so every face has a 3rd chance to face the poles
        is_flip = (random.uniform(0,1)<(2./3.))
        disp = list_distances((x,y,z), loc)
        x = disp[0]
        y = disp[1]
        z = disp[2]
        if is_flip:
            is_flip = (random.uniform(0,1)<0.5)
            if is_flip:
                product.set_rot(90,0,1,0)
                coord_writer.writerow([-z,y,x])
            else:
                product.set_rot(90,1,0,0)
                coord_writer.writerow([x,z,-y])
        else:
            product.set_rot(0,0,1,0)
            coord_writer.writerow([x,y,z])

        # position cube close to subject
        loc2 = loc
        while list_distances(loc, loc2).magnitude < math.sqrt(3):
            loc2 = bld.random_cartesian_coords(0.0,0.0,0.0,2.0,4.0)
        cube2.set_location(loc2)

        render_path = os.path.join(render_folder,'render%d.png'%i)
        scene.render_to_file(render_path)
