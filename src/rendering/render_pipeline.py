# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:51:48 2018

@author: Pavel

Rendering Pipeline. This file contains all necessary calling functions 
for full rendering from object files to final images.
The command for running the script can be found in bottom part of the code.
Two dictionaries of parameters are necessary. One contains the parameters
for Blender and one contains the parameters for Merging.

For more detailed description and example see the appropriate function
and an example at the end of file. 

Run on commmand line using this command
python render_pipeline.py

"""

import sys
from shutil import rmtree, make_archive
from shutil import move as sh_move
from PIL import Image
import numpy as np
import os
import subprocess
import json

"""
Here the paths have to be set up.

The file require other modules from the src folder,
the project_path should point to the folder that contains the src

The rendering process requires obj files and other images.
These should be in render_workspace.
A functioning render_workspace is in the group folder, but feel free
to download it using psftp and place it on your system. 
Do not forget to change the path to render_workspace as it is hard coded.

"""
#boop = '/vol/bitbucket/who11/CO-530/Lobster/src'

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
#project_path = '/vol/bitbucket/who11/CO-530/Lobster/'
#workspace = os.path.join(project_path, "render_workspace")
workspace = '/vol/project/2017/530/g1753002/render_workspace'

#Need to adjust to the local path to Blender executable
#bl_path = "E:\Blender_Foundation\Blender\\blender"

if not project_path in sys.path:
    sys.path.append(project_path)


#sys.path.append("E:/Blender_Foundation/Blender/2.79/python/lib/site-packages/")
#sys.path.append("E:/Anaconda/Lib/site-packages/scipy/")
print(sys.path)
import SceneLib.Merge_Images as mi
import RandomLib.random_background as rb



"""------------ Validate folders ----------- """

# Folders that have to be present or created at the begining of the run
data_folders = ['object_files',
                'bg_database',
                'generate_bg',
                'object_poses',
                'final_folder',
                'final_folder/images',
                'final_zip']

# Folders to be destroyed at the end of the run
temp_folders = ['generate_bg',
                'object_poses', 
                #'final_folder/images',
                'final_folder']

def validate_folders(target_folder, folder_list):
    """
    Check whether all folders in folder_list are present in the target_folder
    If not, create them.
    """
    diff = sorted(list(set(folder_list) - set(os.listdir(target_folder))))
    print("Creating the following folders: ",sorted(diff))
    if not diff == []:
            for folder in diff:
                print("making ", folder)
                os.mkdir(os.path.join(target_folder,folder))


def destroy_folders(target_folder, folder_list):
    """
    Destroy all folders in the target folder that are on the folder list
    """
    for folder in folder_list:
        full_path = os.path.join(target_folder,folder)
        if(os.path.isdir(full_path)):
            rmtree(full_path)

"""------------ Helper functions ----------- """
def generate_poses(src_dir, blender_path, object_folder, output_folder, renders_per_product, blender_attributes):
    """
    Make a system call to Blender, passing the configuration for this run
    and wait for Blender to return.

    args:
        src_dir: full path to project source code, so Blender can add to its path
        blender_path: path the the Blender executable
        object_folder: path to a folder containing folders of .obj files
        output_folder: path to which Blender should save the rendered images
        renders_per_product: number of images to generate per product (.obj file)
        blender_attributes: a dictionary of Blender configurations.

    Passing Rendering Parameters to Blender:
        Rendering parameters should be passed to Blender in a dictionary of the format

        blender_attributes = {
            "attribute_distribution_params": list(list[string, string, float]),
            "attribute_distribution" : list(list(string, dict(string, float, float)))
        }

        Only one of attribute_distribution_params or attribute_distribution
        should be set for each run. Leave the unused element as an empty list.

        Examples:
        "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]]

        "attribute_distribution" : [["lamp_energy", {"dist":"UniformD","l":2000.0,"r":2400.0}]]

        blender_attributes = {
            "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
            "attribute_distribution" : []
        }
    """
    print("Project source dir is", src_dir)
    print("Blender path is ", blender_path)


    blender_script_path = os.path.join(src_dir, 'rendering', 'render_poses.py')
    #config_file_path = os.path.join(src_dir, 'rendering', 'config.json')

    blender_args = [blender_path, '--background', '--python', blender_script_path, '--',
                    src_dir,
                    object_folder,
                    output_folder,
                    str(renders_per_product),
                    json.dumps(blender_attributes)]

    print('Rendering...')
    subprocess.check_call(blender_args)
    print('Rendering done!')


def gen_merge(image, save_as, pixels=300):
    """
    This functionw will be called whenever you need to generate your own
    background. Instead of generating large quanta and randomly searching
    it will generate one background for each image. Thus it will be faster
    and definitely uniquely random.

    !!Careful, the save_as should be full path including the name
    e.g. foo/bar/image1.jpg
    args:
        image: a PIL Image type of the object pose
        save_as: a full path (including a name of the image) to which the final 
            image should be saved
        pixels: The number of pixels the final square image will have.
            Default = 300
    """

    back = rb.rand_background(np.random.randint(2,4),pixels)
    scaled = back*256
    background = Image.fromarray(scaled.astype('uint8'), mode = "RGB")
    final = mi.merge_images(image, background)

    try:
        final.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
    except IOError:
        print("IO error")
    except KeyError:
        print("Key error")


def full_run(zip_name, obj_set, blender_path, renders_per_class=10, work_dir=workspace, generate_background=True, background_database=None, blender_attributes={}):
    """
    Function that will take all the parameters and execute the
    appropriate pipeline

    args:
        work_dir : path to the workspace that contains individual folders
        generate_background : Flag, if True, we will generate random background
                if False, we will use images in a given database
        background_database : Path to databse of backgrounds to use if
            generate_background is False
    """
    print('Checking data directories...')

    # Ensure render_workspace folder exists
    if not os.path.isdir(workspace):
        print("Can't find rendering workspace folder. Please create the folder",
        workspace, ", containing object files and background database. See " \
        "group folder for example.")
        return

    validate_folders(work_dir, data_folders)

    obj_poses = os.path.join(work_dir, "object_poses")

    """----------------- Generating object poses ---------------"""
    src_path = os.path.join(project_path, "src")
    generate_poses(src_path, blender_path, obj_set, obj_poses, renders_per_class, blender_attributes)

    #now we need to take Ong' stats and move them into final folder
    for folder in os.listdir(obj_poses):
        orig_stats=os.path.join(obj_poses,folder,"stats")      

        if(os.path.isdir(orig_stats)):
            final_name= folder + "_stats"
            sh_move(orig_stats, os.path.join(work_dir,"final_folder" ,final_name))

    """----------------- Generating final images ---------------"""
    """
    We need to distinguish between the case of drawing backrounds
    from a database and when generating ourselves
    """
    final_folder = os.path.join(work_dir, "final_folder")
    final_im = os.path.join(work_dir, "final_folder/images")
    # Generate images for each class poses
    for folder in os.listdir(obj_poses):
        sub_obj = os.path.join(obj_poses, folder)
        if os.path.isdir(sub_obj) is False:
            print(sub_obj, " is not a folder")
            continue
        
        sub_final = os.path.join(final_im, folder)
        os.mkdir(sub_final)
        
        # Merge images based on the choice of background
        if(generate_background):
            # for each object pose
            for image in os.listdir(sub_obj):
                path = os.path.join(sub_obj, image)
                try:
                    foreground = Image.open(path)
                except:
                    print("skipping", image)
                    continue

                just_name = os.path.splitext(image)[0]
                name_jpg = just_name + ".jpg"
                save_to = os.path.join(sub_final, name_jpg)
                gen_merge(foreground, save_to, pixels = 300)
                foreground.close()

        elif(generate_background is False and background_database is None):
            print("We need a background database")
            return
        else:
            # We generate a random mesh background
            mi.generate_for_all_objects(sub_obj,background_database ,sub_final)


    for folder in os.listdir(obj_poses):
        print(folder)
    # export everything into a zip file
    make_archive(zip_name, 'zip',final_folder)
    destroy_folders(work_dir, temp_folders)

"""
The blender parameters. Keywords should be self explanatory. 
For more details ask Ong.
A default parameters can be used by passing an empty dictionary
blender_attributes={}
"""

"""------------------ Running the pipeline ------------------"""

blender_attributes = {
    "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
    "attribute_distribution" : []
}


# Default paths
# Set path for final zip file containing training data
zip_save1 = os.path.join(workspace, "final_zip/sun_bg_data")
zip_save2 = os.path.join(workspace, "final_zip/random_bg_data")

# Set backround image database path
background_database = os.path.join(workspace, "bg_database/SUN_back/")

# Set object file path
obj_set = os.path.join(workspace, "object_files/two_set")

# Set Blender path
bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
#bl_path = "E:\Blender_Foundation\Blender\\blender" # for Pavel

# Construct rendering parameters
argument_list = []

arguments1 = {
    "zip_name": zip_save1,
    "obj_set": obj_set,
    "blender_path": bl_path,
    "renders_per_class": 2,
    "work_dir": workspace,
    "generate_background": False,
    "background_database": background_database,
    "blender_attributes": blender_attributes
    }

arguments2 = {
    "zip_name": zip_save2,
    "obj_set": obj_set,
    "blender_path": bl_path,
    "renders_per_class": 2,
    "work_dir": workspace,
    "generate_background": True,
    "background_database": background_database,
    "blender_attributes": blender_attributes
    }

argument_list.append(arguments1)
argument_list.append(arguments2)
#argument_list.append(arguments3)

for value in argument_list:
    full_run(**value)
    print("One run done")
