import sys
import argparse
import json
import bpy
import os
from io import StringIO

# set use GPU
"""
C = bpy.context
C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
C.user_preferences.addons['cycles'].preferences.devices[0].use = True
C.scene.render.engine = 'CYCLES'
"""


"""" --------------- CLI setup ------------- """
# CLI code from https://developer.blender.org/diffusion/B/browse/master/release/scripts/templates_py/background_job.py

# get the args passed to blender after "--", all of which are ignored by
# blender so scripts may receive their own arguments
argv = sys.argv

if "--" not in argv:
    argv = []  # as if no args are passed
else:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

# When --help or no args are given, print this help
usage_text = (
    "Run blender in background mode with this script:"
    "  blender --background --python " + __file__ + " -- [options]"
)

"""Helper functions"""
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

"""" --------------- Arguments ------------- """
parser = argparse.ArgumentParser(description=usage_text)

parser.add_argument('project_dir',
                    help='path to source code')

parser.add_argument('object_folder',
                    help='path to folder containing object files')

parser.add_argument('output_folder',
                    help='path to folder to which poses should be saved')

parser.add_argument('renders_per_product', type=int, default=1,
                    help='number of renders to per product')

parser.add_argument('render_resolution', type=int, default=300,
                    help='resolution of rendered object pose')

parser.add_argument('blender_attributes',
                    help='json dump of blender attributes')

parser.add_argument("visualize_dump", type=str2bool, default=False,
                        help="visualization of blender parameters")

parser.add_argument('dry_run_mode', type=str2bool, default=False,
                    help='json dump of blender attributes')

args = parser.parse_args(argv)

if not argv:
    parser.print_help()
    exit(-1)

# print(args)

"""" --------------- Blender Setup ------------- """
# Ensure source directory in Blender python path
sys.path.append(os.path.join(args.project_dir))

import rendering.RenderInterface as Render


"""" --------------- Blender Setup ------------- """
if args.blender_attributes:
    io = StringIO(args.blender_attributes)
    blender_attributes = json.load(io)

print('Running blender with the following parameters: \n {} \n'.format(blender_attributes))


"""" --------------- Helper functions for folder navigation ------------- """
def find_model(product_folder):
    """Return the name of the .model file in a folder"""
    for file in os.listdir(product_folder):
        if file.endswith('.model'):
            return file


"""" --------------- Rendering ------------- """
RI = Render.RenderInterface(num_images=args.renders_per_product, resolution=args.render_resolution)

for product in os.listdir(args.object_folder):
    product_folder = os.path.join(args.object_folder, product)

    # Validate object
    if not os.path.isdir(product_folder):
        print("RENDER POSES: Couldn't find {} object folder! Skipping".format(product))
        continue

    # Create product folder in object_renders
    render_folder = os.path.join(args.output_folder, product)
    if not os.path.isdir(render_folder):
        print('RENDER POSES: Making render folder', render_folder)
        os.mkdir(render_folder)

    # Get model files
    model_file = find_model(product_folder)

    # Configure model paths
    model_path = os.path.join(product_folder, model_file)

    print("RENDER POSES: Detected model, using model: \n {}".format(model_path))
    print("RENDER POSES: Render folder used : \n {} \n".format(render_folder))

    # Do the blender stuff
    RI.load_from_model(model_path, render_folder)

    if blender_attributes:
        print("RENDER POSES: the following attributes are supplied for this run: ")
        for param in blender_attributes['attribute_distribution_params']:
            print(param)
            RI.set_attribute_distribution_params(param[0], param[1], param[2])

        for dist in blender_attributes['attribute_distribution']:
            print(dist)
            RI.set_attribute_distribution(dist[0], dist[1])

        print("\n")

    print("RENDER POSES: begin rendering {} \n".format(product))
    RI.render_all(dump_logs=True, visualize=args.visualize_dump, dry_run=args.dry_run_mode)
    print("RENDER POSES: finished rendering {} \n".format(product))