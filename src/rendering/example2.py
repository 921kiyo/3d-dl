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
boop = 'D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/src/rendering/BlenderAPI'


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
num_images = 1000
# required file paths for the script to run
obj_path = 'D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\objects\\Halloumi\\Halloumi.obj'
texture_path = 'D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\objects\\Halloumi\\Halloumi.jpg'
render_folder = 'D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\object_poses\\Halloumi_white'
#render_folder = '/vol/bitbucket/who11/CO-530/data/Clinique/render'
csv_path = os.path.join(render_folder,'camera.csv')

# Import the shape, and give texture image
product = bld.BlenderImportedShape(obj_path=obj_path, location=(-1,0,-1) ,orientation=(0,0,1,0))
product.add_image_texture(texture_path)
product.set_diffuse(color=(1,0,0,1),rough=0.1)
product.set_gloss(rough=0.1)
product.set_mixer(0.3)
product.set_scale((1.,1.,1.))
product.toggle_smooth()

# Create a cube
"""
cube = bld.BlenderCube(location = (3,3,3))
cube.set_scale((.5,.5,.5))
cube.set_diffuse(color=(0,0,1,1),rough=0.1)
cube.set_gloss(rough=0.1)
cube.set_mixer(0.3)
"""
Lamps = []
# Fetch the camera and lamp
cam = bld.BlenderCamera(bpy.data.objects['Camera'])
Lamps.append(bld.BlenderPoint(bpy.data.objects['Lamp']))

# Create a 2nd and 3rd lamp
Lamps.append(bld.BlenderPoint(None))
Lamps.append(bld.BlenderPoint(None))

# instantiate scene
scene = bld.BlenderScene(bpy.data.scenes[0])
scene.set_render()

with open(csv_path,'w') as csvfile:

    coord_writer = csv.writer(csvfile, delimiter=',')

    for i in range(num_images):

        # **********************  LIGHTS **********************
        # turn everything off
        for lamp in Lamps:
            lamp.turn_off()

        # set random lighting conditions
        num_lamps = random.randint(1,3)
        for l in range(num_lamps):
            lamp = Lamps[l]
            lamp.turn_on()
            lamp.random_lighting_conditions()
            x, y, z = bld.random_shell_coords(5.0)
            lamp.set_location(x, y, z)

        # **********************  CAMERA **********************
        # random location of camera along shell coordinates
        x,y,z = bld.random_shell_coords(7.0)
        cam.set_location(x,y,z)
        # face towards the centre
        cam.face_towards(0.0,0.0,0.0)

        # randomize spin of camera
        spin_angle = random.uniform(0.0,360.0)
        cam.spin(spin_angle)

        # **********************  ACTION **********************
        loc = bld.random_cartesian_coords(0.0,0.0,0.0,1.0,4.0)
        product.set_location(*loc)

        # flip subject 90 degrees along one axis, so every face has a 3rd chance to face the poles
        is_flip = random.randint(1,3)
        disp = list_distances((x,y,z), loc)
        x = disp[0]
        y = disp[1]
        z = disp[2]
        if is_flip == 1:
            product.set_rot(90,0,1,0)
            coord_writer.writerow([-z,y,x])
        elif is_flip == 2:
            product.set_rot(90,1,0,0)
            coord_writer.writerow([x,z,-y])
        else:
            product.set_rot(0,0,1,0)
            coord_writer.writerow([x,y,z])

        # position cube close to subject
        loc2 = loc
        while list_distances(loc, loc2).magnitude < math.sqrt(3):
            loc2 = bld.random_cartesian_coords(0.0,0.0,0.0,2.0,4.0)
        #cube.set_location(*loc2)

        # **********************  RENDER N SAVE **********************
        render_path = os.path.join(render_folder,'render%d.png'%i)
        scene.render_to_file(render_path)
