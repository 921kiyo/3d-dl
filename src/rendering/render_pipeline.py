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

# set use GPU
"""
C = bpy.context
C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
C.user_preferences.addons['cycles'].preferences.devices[0].use = True
C.scene.render.engine = 'CYCLES'
"""

"""
Here the paths have to be set up.
In the case that you are running this on your system, you should have
a directory "render_workspace" with all the necessary files in the same
folder as is the folder src

If you are running this with the files being in group directory, while this
script itself is not in the directory, you should change the path
"workspace" to wherever this "render_workspace is"

Pavel will test it and add further instructions here
"""
#boop = '/vol/bitbucket/who11/CO-530/Lobster/src'
# ocado_folder = '/vol/bitbucket/who11/CO-530/Lobster/src'
dir_path = os.path.dirname(os.path.realpath(__file__)) # the src folder
rend_folder = os.path.abspath(os.path.join(dir_path, os.pardir))
ocado_folder = os.path.abspath(os.path.join(rend_folder,os.pardir))
workspace  = os.path.join(ocado_folder, "render_workspace")
# workspace = '/vol/bitbucket/who11/CO-530/Lobster/render_workspace'

#Need to adjust to the local path to Blender executable
bl_path = "E:\Blender_Foundation\Blender\\blender"




if not (ocado_folder in sys.path):
    sys.path.append(ocado_folder)


import src.rendering.SceneLib.Merge_Images as mi
import src.rendering.RandomLib.random_background as rb


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

def generate_poses(src_dir, blender_path, object_folder, output_folder, renders_per_product, blender_attributes):

    """
    This function will call Blender to Generate object poses
    It needs to be supplied with the path to the src folder, the blender executable.
    It will create poses for each folder in the object_folder.
    There will be "renders_per_product" poses for each product (e.g. for each
    folder in the object_folder).
    The last attributes is a dictionary of parameters for Blender,
    see example for the details of these parameters.
    The blender_attributes can also be left as an empty dictionary in which case
    a default set of parameters will be used
    """
    print("src dir is", src_dir)
    print("blender path is ", blender_path)

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


def gen_merge(image, save_as, pixels = 300):
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


def full_run(zip_name,  obj_set, blender_path, renders_per_class = 10, work_dir = workspace, generate_background = True, backgr_dat = None, blender_attributes = {} ):
    """
    Function that will take all the parameters and execute the
    appropriate pipeline

    args:
        work_dir : path to the workspace that contains individual folders
        generate_background : Flag, if True, we will generate random background
                if False, we will use images in a given database
        backgr_dat : Path to databse of backgrounds to use if
            generate_background is False
    """

    print('Checking data directories...')

    validate_folders(work_dir,data_folders)

    obj_poses = os.path.join(work_dir, "object_poses")


    """
    code to generate object poses
    """
    src_path = os.path.join(ocado_folder, "src")
    print("src path is", src_path)
    generate_poses(src_path, blender_path, obj_set, obj_poses, renders_per_class, blender_attributes)
    
    #now we need to take Ong' stats and move them into final folder
    for folder in os.listdir(obj_poses):
        orig_stats=os.path.join(obj_poses,folder,"stats")      
        if(os.path.isdir(orig_stats)):
            final_name= folder + "_stats"
            sh_move(orig_stats, os.path.join(work_dir,"final_folder" ,final_name))

    """------------------------Code to generate final images----------"""
    """
    We need to distinguish between the case of drawing backrounds
    from a database and when generating ourselves
    """
    final_folder = os.path.join(work_dir, "final_folder")
    final_im = os.path.join(work_dir, "final_folder/images")
    # Generate images for each class poses
    for folder in os.listdir(obj_poses):
        sub_obj = os.path.join(obj_poses, folder)
        if(os.path.isdir(sub_obj) is False):
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
                    foreground=Image.open(path)
                except:
                    print("skipping", image)
                    continue

                just_name = os.path.splitext(image)[0]
                name_jpg = just_name+".jpg"
                save_to = os.path.join(sub_final, name_jpg)
                gen_merge(foreground, save_to, pixels = 300)
                foreground.close()

        elif(generate_background is False and backgr_dat is None):
            print("We need a background database")
            return
        else:
            # We generate a random mesh background
            mi.generate_for_all_objects(sub_obj,backgr_dat ,sub_final)

    
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
blender_attributes = {
    "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
    "attribute_distribution" : []
}


"""zip files name"""
"""
One zip file contain all images from the given run
It is possible and adviced to general several tests at once
"""
zip_save1 = os.path.join(workspace, "final_zip/sun_bg_data")
zip_save2 = os.path.join(workspace, "final_zip/random_bg_data")
zip_save3 = os.path.join(workspace, "final_zip/white_bg_data")


# Set up paths to background databases and which set of object files
# is to be used for generation
backg_database = os.path.join(workspace,"bg_database/SUN_back/")
white_background = os.path.join(workspace, "bg_database/white/")
obj_set = os.path.join(workspace, "object_files/two_set")


argument_list = [] # Create a list of dictionaries
arguments1 = {"zip_name": zip_save1, "obj_set": obj_set ,"blender_path": bl_path,"renders_per_class": 2,"work_dir": workspace, "generate_background": False, "backgr_dat": backg_database, "blender_attributes": blender_attributes}
arguments2 = {"zip_name": zip_save2, "obj_set": obj_set ,"blender_path": bl_path,"renders_per_class": 2,"work_dir": workspace, "generate_background": True, "backgr_dat": backg_database, "blender_attributes": blender_attributes}
arguments3 = {"zip_name": zip_save3, "obj_set": obj_set ,"blender_path": bl_path,"renders_per_class": 2,"work_dir": workspace, "generate_background": False, "backgr_dat": white_background, "blender_attributes": blender_attributes}
argument_list.append(arguments1)
argument_list.append(arguments2)
argument_list.append(arguments3)

for value in argument_list:
    full_run(**value)
    print("One run done")

    