# -*- coding: utf-8 -*-
import sys
import os
from copy import copy
import itertools

from rendering.render_pipeline import full_run_with_notifications

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
#workspace = '/vol/bitbucket/who11/CO-530/render_workspace' # bitbucket storage
workspace = 'D:\\PycharmProjects\\Lobster\\data\\render_workspace' # for Ong
# Set Blender path
#bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
bl_path = 'D:\\Program Files\\Blender Foundation\\Blender\\blender' # for Ong
# Set of objects to work with
obj_set = os.path.join(workspace, 'object_files','ten_set_model_format')
# Set backround image database path
background_database = os.path.join(workspace, 'bg_database','SUN_back')


"""------------------ Lighting parameters ------------------"""
''' hand-chosen lighting parameters '''
attribute_distribution_params = [
    # lighting parameter set 2
    # 1 <= num lamps <= 10, medium energy with high variation, equates to highly varied lighting conditions

    ["num_lamps","mid", 5], ["num_lamps","scale", 0.4],
    ["lamp_energy", "mu", 1250.0], ["lamp_energy", "sigmu", 0.6],
    # camera parameter set 1
    # medium radius, larger variation, varied sized subjects
    ["camera_loc","phi_sigma", 10.0],
    ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.5], ["camera_radius", "r", 10]
]
N_samples = 100

arguments_list = []
# datapoint 1: 10,000 images, 64 samples
"""
arguments_list.append(
    {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": N_samples,
        "work_dir": workspace,
        "generate_background": False,
        "background_database": background_database,
        "blender_attributes": {
            "attribute_distribution_params": copy(attribute_distribution_params),
            "attribute_distribution": []
        },
        "dry_run_mode": False,
        "render_samples": 64
    }
)
"""
# datapoint 2: 10,000 images, 128 samples
arguments_list.append(
    {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": N_samples,
        "work_dir": workspace,
        "generate_background": False,
        "background_database": background_database,
        "blender_attributes": {
            "attribute_distribution_params": copy(attribute_distribution_params),
            "attribute_distribution": []
        },
        "dry_run_mode": False,
        "render_samples": 128
    }
)

for arguments in arguments_list:
    full_run_with_notifications(**arguments)
    print("One run complete! \n")
