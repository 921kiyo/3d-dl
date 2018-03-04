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

boop = 'D:/PycharmProjects/Lobster/src/'

if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld
""" ************* User specified stuff here ************* """
# Specify number of images to render

num_images = 5
# required file paths for the script to run
obj_path = 'D:\\PycharmProjects\\3DModels\\Tea\\Tea.obj'
texture_path = 'D:\\PycharmProjects\\3DModels\\Tea\\Tea.jpg'
render_folder = 'D:\\PycharmProjects\\3DModels\\Tea\\render'

csv_path = os.path.join(render_folder,'camera.csv')

# instantiate scene
scene = bld.BlenderRandomScene(bpy)

# delete the initial cube
cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
cube.delete()

# Fetch the camera and lamp
cam = bld.BlenderCamera(bpy.data.objects['Camera'])
scene.load_subject_from_path(obj_path=obj_path, texture_path=texture_path)
scene.set_render()
scene.add_camera(cam)

for i in range(num_images):
    # **********************  RENDER N SAVE **********************
    render_path = os.path.join(render_folder,'render%d.png'%i)
    scene.render_to_file(render_path)

scene.set_attribute_distribution_params('num_lamps','l',5)
scene.set_attribute_distribution_params('num_lamps','r',8)
scene.set_attribute_distribution_params('lamp_energy','mu',500.0)
scene.set_attribute_distribution_params('lamp_size','mu',5.)
scene.set_attribute_distribution_params('camera_radius','sigmu',0.1)

for i in range(num_images, num_images*2):
    # **********************  RENDER N SAVE **********************
    render_path = os.path.join(render_folder,'render%d.png'%i)
    scene.render_to_file(render_path)

print(scene.retrieve_logs())
