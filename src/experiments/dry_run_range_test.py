# -*- coding: utf-8 -*-
import sys
import os
from copy import copy
import itertools
import numpy as np

from rendering.render_pipeline import full_run

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
workspace = 'D:\\PycharmProjects\\Lobster\\data\\render_workspace' # for Ong
# Set Blender path
bl_path = 'D:\\Program Files\\Blender Foundation\\Blender\\blender' # for Ong
# Set of objects to work with
obj_set = os.path.join(workspace, 'object_files','two_set_model_format')
# Set backround image database path
background_database = os.path.join(workspace, 'bg_database','SUN_back')

if not project_path in sys.path:
    sys.path.append(project_path)

"""------------------ Running the pipeline ------------------"""
# Test all corners of the search space
arguments_list = []
corners = itertools.product([1,20],[0.0,1.0],[0.0,30000.0],[0.0,3.0],[0.0,30.0],[3.0,12.0],[0.0,3.0])
for corner in corners:
    attribute_distribution_params = []

    attribute_distribution_params.append(["num_lamps", "mid", corner[0]])
    attribute_distribution_params.append(["num_lamps", "scale", corner[1]])
    attribute_distribution_params.append(["lamp_energy", "mu", corner[2]])
    attribute_distribution_params.append(["lamp_energy", "sigmu", corner[3]])

    attribute_distribution_params.append(["camera_loc", "phi_sigma", corner[4]])
    attribute_distribution_params.append(["camera_radius", "mu", corner[5]])
    attribute_distribution_params.append(["camera_radius", "sigmu", corner[6]])

    # blender_attributes encompass pose generation
    arguments_list.append(
        {
            "obj_set": obj_set,
            "blender_path": bl_path,
            "renders_per_class": 10,
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


# Test 50 random points in the search space
for arguments in arguments_list:
    full_run(**arguments)

arguments_list = []
for i in range(50):

    attribute_distribution_params = []

    attribute_distribution_params.append(["num_lamps","mid",np.random.randint(1,20)])
    attribute_distribution_params.append(["num_lamps", "scale", np.random.uniform(0.0, 1.0)])
    attribute_distribution_params.append(["lamp_energy", "mu", np.random.uniform(0.0, 30000.0)])
    attribute_distribution_params.append(["lamp_energy", "sigmu", np.random.uniform(0.0, 3.0)])

    attribute_distribution_params.append(["camera_loc", "phi_sigma", np.random.uniform(0.0, 30.0)])
    attribute_distribution_params.append(["camera_radius", "mu", np.random.uniform(3.0, 12.0)])
    attribute_distribution_params.append(["camera_radius", "sigmu", np.random.uniform(0.0, 3.0)])


    # blender_attributes encompass pose generation
    arguments_list.append(
        {
            "obj_set": obj_set,
            "blender_path": bl_path,
            "renders_per_class": 10,
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
