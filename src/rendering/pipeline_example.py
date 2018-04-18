# -*- coding: utf-8 -*-
import sys
import os

from rendering.render_pipeline import full_run

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
# workspace = '/vol/project/2017/530/g1753002/render_workspace'
workspace = 'D:\\PycharmProjects\\Lobster\\data\\render_workspace' #for Ong
# Set Blender path
# bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
bl_path = 'D:\\Program Files\\Blender Foundation\\Blender\\blender' # for Ong
# Set of objects to work with
obj_set = os.path.join(workspace, 'object_files','ten_set_model_format')
# Set backround image database path
background_database = os.path.join(workspace, 'bg_database','SUN_back')

if not project_path in sys.path:
    sys.path.append(project_path)


"""------------------ Running the pipeline ------------------"""

# blender_attributes encompass pose generation
blender_attributes = {
    "attribute_distribution_params":
        [

            # number of lamps is a DISCRETE UNIFORM DISTRIBUTION over NON_NEGATIVE INTEGERS,
            # params l and r are lower and upper bounds of distributions, need to be positive integers
            ["num_lamps","mid", 6], ["num_lamps","scale", 0.4],

            # lamp distance is a TRUNCATED NORMAL DISTRIBUTION over NON-NEGATIVE INTEGERS,
            # param mu is mean , must be non-negative,
            # sigmu is the value of sigma taken as a proportion of the mean, must also be non-negative,
            # l and r are the lower and upper bounds of the lamp distances respectively - l >= r always.
            # both need to be non-negative
            # r can be set to None to indicate that r is infinity
            ["lamp_distance", "mu", 5.0], ["lamp_distance", "sigmu", 0.0], ["lamp_distance", "l", 0.0], ["lamp_distance", "r", None],

            # lamp energy is a TRUNCATED NORMAL DISTRIBUTION, param descriptions same as above
            ["lamp_energy", "mu", 2000.0], ["lamp_energy", "sigmu", 0.3], ["lamp_energy", "l", 0.0], ["lamp_energy", "r", None],

            # lamp size is a TRUNCATED NORMAL DISTRIBUTION, param descriptions same as above
            ["lamp_size", "mu", 5.0], ["lamp_size", "sigmu", 0.3], ["lamp_size", "l", 0.0], ["lamp_size", "r", None],

            # camera location is a COMPOSITE SHELL RING DISTRIBUTION
            # param normals define which rings to use, based on their normals, permitted values are 'X','Y','Z' and a combination of the three
            # phi sigma needs to be non-negative, and defines the spread of the ring in terms of degrees
            # phi sigma of roughly 30.0 corresponds to a unifrom sphere
            ["camera_loc","phi_sigma", 10.0], ["camera_loc","normals", "YZ"],

            #camera radius is a Truncated Normal Distribution
            ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.3], ["camera_radius", "l", 0.0], ["camera_radius", "r", None]
        ],
    "attribute_distribution" : []
}

# everything else here is about background parameters
arguments = {
    "obj_set": obj_set,
    "blender_path": bl_path,
    "renders_per_class": 20,
    "work_dir": workspace,
    "generate_background": True,
    "background_database": background_database,
    "blender_attributes": blender_attributes,
    }

full_run(**arguments)

