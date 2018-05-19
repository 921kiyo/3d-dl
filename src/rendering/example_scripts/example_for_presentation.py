"""
This example script creates a box in the middle of a half room
"""

import sys
import os
import bpy
import numpy as np

# set use GPU
C = bpy.context
C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
C.user_preferences.addons['cycles'].preferences.devices[0].use = True
C.scene.render.engine = 'CYCLES'

# path to blender library
boop = '/vol/bitbucket/who11/CO-530/Lobster/src'


if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld

# delete the initial cube
cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
cube.delete()

""" ************* User specified stuff here ************* """
num_images = 50
# required file paths for the script to run
obj_path = 'D:\\PycharmProjects\\3DModels\\Ocado\\MangoYogurt\\MangoYogurtTop_redo\\MangoYogurtTop.obj'
texture_path = 'D:\\PycharmProjects\\3DModels\\Ocado\\MangoYogurt\\MangoYogurtTop_redo\\MangoYogurtTop_shopped.jpg'
render_folder = 'D:\\PycharmProjects\\3DModels\\Ocado\\MangoYogurt\\MangoYogurtTop_redo\\render'
bg_folder = 'D:\\PycharmProjects\\Lobster\\data\\render_workspace\\bg_database\\white'
final_folder = 'D:\\PycharmProjects\\3DModels\\Ocado\\MangoYogurt\\MangoYogurtBot\\render_bg'

# Import the shape, and give texture image
product = bld.BlenderImportedShape(obj_path=obj_path, location=(-1,0,-1) ,orientation=(180,0,1,0))
product.set_mesh_bbvol(8.0) # size of original cube
product.add_image_texture(texture_path)
product.set_diffuse(color=(1,0,0,1),rough=0.1)
product.set_gloss(rough=0.1)
product.set_mixer(0.1)
product.toggle_smooth()
product.set_location(0.,0.,0.)

# Create a cube
Lamps = []
# Fetch the camera and lamp
cam = bld.BlenderCamera(bpy.data.objects['Camera'])
Lamps.append(bld.BlenderPoint(bpy.data.objects['Lamp']))

# Create a 2nd and 3rd lamp
for i in range(7):
    Lamps.append(bld.BlenderPoint(None))

lamp_locations = [(5,5,5),(-5,5,5),(5,-5,5),(5,5,-5),(5,-5,-5),(-5,5,-5),(-5,-5,5),(-5,-5,-5)]

for loc,lamp in zip(lamp_locations, Lamps):
    lamp.turn_on()
    lamp.set_brightness(2500)
    lamp.set_size(5)
    lamp.set_location(*loc)

# instantiate scene
scene = bld.BlenderScene(bpy.data.scenes[0])
scene.set_render(resolution=512, samples=256)

theta = np.linspace(0.0, 360.0, 360)
r = 5.0
cam.set_location(5.0,0.0,0.0)
cam.face_towards(0.0,0.0,0.0)
#product.rotate(135.0,0.0,0.0,1.0)
for t in theta:
    # **********************  CAMERA **********************
    # random location of camera along shell coordinates
    product.rotate(1.0,0.0,1.0,0.0)

    # **********************  RENDER N SAVE **********************
    render_path = os.path.join(render_folder,'render%d.png'%t)
    scene.render_to_file(render_path)

