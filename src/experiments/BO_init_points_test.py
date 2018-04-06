# -*- coding: utf-8 -*-
import sys
import os
from copy import copy
import itertools

from rendering.render_pipeline import full_run

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
workspace = 'D:\\PycharmProjects\\Lobster\\data\\render_workspace' # for Ong
# Set Blender path
bl_path = 'D:\\Program Files\\Blender Foundation\\Blender\\blender' # for Ong
# Set of objects to work with
obj_set = os.path.join(workspace, 'object_files','ten_set_model_format')
# Set backround image database path
background_database = os.path.join(workspace, 'bg_database','SUN_back')

if not project_path in sys.path:
    sys.path.append(project_path)


"""------------------ Lighting parameters ------------------"""
''' hand-chosen lighting parameters '''
lighting_params = [
    # lighting parameter set 0
    # 8 <= num lamps <= 10, medium-low energy with little variation, equates to even lighting
    [
        ["num_lamps","mid", 9], ["num_lamps","scale", 0.15],
        ["lamp_energy", "mu", 500.0], ["lamp_energy", "sigmu", 0.1]
    ],
    # lighting parameter set 1
    # 1 <= num lamps <= 3, high energy with little variation, equates to stronger directional lighting
    [
        ["num_lamps","mid", 2], ["num_lamps","scale", 0.5],
        ["lamp_energy", "mu", 2000.0], ["lamp_energy", "sigmu", 0.1]
    ],
    # lighting parameter set 2
    # 1 <= num lamps <= 10, medium energy with high variation, equates to highly varied lighting conditions
    [
        ["num_lamps","mid", 5], ["num_lamps","scale", 0.8],
        ["lamp_energy", "mu", 1000.0], ["lamp_energy", "sigmu", 0.6]
    ],
]


"""------------------ Camera parameters ------------------"""
''' hand-chosen camera parameters '''
camera_params = [
    # camera parameter set 0
    # medium radius, little variation, fixed, medium sized subjects
    [
        ["camera_loc","phi_sigma", 10.0],
        ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.1]
    ],
    # camera parameter set 1
    # medium radius, larger variation, varied sized subjects
    [
        ["camera_loc","phi_sigma", 10.0],
        ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.4]
    ]
]

"""------------------ Running the pipeline ------------------"""
arguments_list = []
for (lighting_param, camera_param) in itertools.product(lighting_params, camera_params):

    attribute_distribution_params = []
    attribute_distribution_params.extend(lighting_param)
    attribute_distribution_params.extend(camera_param)

    # blender_attributes encompass pose generation
    arguments_list.append(
        {
            "obj_set": obj_set,
            "blender_path": bl_path,
            "renders_per_class": 1,
            "work_dir": workspace,
            "generate_background": False,
            "background_database": background_database,
            "blender_attributes": {
                "attribute_distribution_params": copy(attribute_distribution_params),
                "attribute_distribution": []
            },
            "dry_run_mode": True
        }
    )

for arguments in arguments_list:
    full_run(**arguments)

