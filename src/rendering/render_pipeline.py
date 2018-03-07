# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:51:48 2018

@author: Pavel

Run on commmand line using this command
blender --background --python render_pipeline.py

"""

import sys
#import random
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
# path to blender library

#boop = 'D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/src/rendering/BlenderAPI'
# above is for Pavel so he does not have to set it every time
#boop = 'D:/PycharmProjects/Lobster/src/'
#boop = '/vol/bitbucket/who11/CO-530/Lobster/src'
dir_path = os.path.dirname(os.path.realpath(__file__)) # the src folder
rend_folder = os.path.abspath(os.path.join(dir_path, os.pardir))
ocado_folder = os.path.abspath(os.path.join(rend_folder,os.pardir))
workspace  = os.path.join(ocado_folder, "render_workspace")

if not (ocado_folder in sys.path):
    sys.path.append(ocado_folder)

#
#sys.path.append("E:/Blender_Foundation/Blender/2.79/python/lib/site-packages/")
#sys.path.append("E:/Anaconda/Lib/site-packages/scipy/")

import src.rendering.SceneLib.Merge_Images as mi
import src.rendering.RandomLib.random_background as rb

""" --------------- CLI setup ------------- """
"""
parser = argparse.ArgumentParser(description='Create training images from 3D models and background images')

#parser.add_argument('data_directory',
 #                   help='path to the data folder')


parser.add_argument('-r', '--render',
                    help='render poses with Blender [number of renders to per product]')


parser.add_argument('-i', '--images',
                    help='generate random background images [number of images]')


parser.add_argument('-m', '--merge', action='store_true',
                    help='merge each render with random background image')


parser.add_argument('-g', '--gpu', action='store_true',
                    help='render with GPU')

args = parser.parse_args()

#print(args)
"""

"""------------ Validate data path and content folders ----------- """

data_folders = ['object_files',
                'bg_database',
                'generate_bg',
                'object_poses',
                'final_folder',
                'final_folder/images',
                'final_zip']

temp_folders = ['generate_bg',
                'object_poses', #  for testing, otherwise uncomment
                #'final_folder/images',
                'final_folder']


def confirm_action(question):
    """Return True if user agrees to question """
    while "Invalid answer. Type 'y' or 'n' then return.":
        reply = input(question + ' (y/n): ').lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def validate_path():
    """Check working directory"""
    try:
        os.chdir(args.data_directory)

    except FileNotFoundError:
        print("Couldn't find the data folder!\n")
        raise


def validate_folders(target_folder, folder_list):
    """Check whether appropriate data folders are there or prompt user to create"""
    #found = os.listdir(target_folder)
    diff = sorted(list(set(folder_list) - set(os.listdir(target_folder))))
    print(os.listdir(target_folder))
    print(sorted(diff))
    if not diff == []:
            for folder in diff:
                print("making ", folder)
                os.mkdir(os.path.join(target_folder,folder))

def destroy_folders(target_folder, folder_list):
    for folder in folder_list:
        full_path = os.path.join(target_folder,folder)
        if(os.path.isdir(full_path)):
            rmtree(full_path)

"""
only one of attribute_distribution_params or attribute_distribution can be set of each run
leave the unused element as an empty list, as below

attribute_distribution_params: list(list[string, string, float])
attribute_distribution: list(list(string, dict(string, float, float)))
"""

# "attribute_distribution" : [["lamp_energy", {"dist":"UniformD","l":2000.0,"r":2400.0}]]

def generate_poses(src_dir, blender_path, object_folder, output_folder, renders_per_product, blender_attributes):

    """
    This function will call Blender to Generate object poses
    """
    #src_dir =
    #blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender'
    print("src dir is", src_dir)
    print("blender path is ", blender_path)

    blender_script_path = os.path.join(src_dir, 'rendering', 'render_poses.py')
    config_file_path = os.path.join(src_dir, 'rendering', 'config.json')

    blender_args = [blender_path, '--background', '--python', blender_script_path, '--',
                    src_dir,
                    object_folder,
                    output_folder,
                    str(renders_per_product),
                    json.dumps(blender_attributes)]

    # blender_args = [blender_path, '--background', '--python']

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
    orig_stats=os.path.join(obj_poses,"stats")
    #os.mkdir(orig_stats)
    
    final_folder = os.path.join(work_dir, "final_folder")
    if(os.path.isdir(orig_stats)):
        sh_move(orig_stats, os.path.join(final_folder, "stats"))

    """------------------------Code to generate final images----------"""
    """
    We need to distinguish between the case of drawing backrounds
    from a database and when generating ourselves
    """

    
    final_im = os.path.join(work_dir, "final_folder/images")
    for folder in os.listdir(obj_poses):
        sub_obj = os.path.join(obj_poses, folder)
        if(os.path.isdir(sub_obj) is False):
            print(sub_obj, " is not a folder")
            continue
        sub_final = os.path.join(final_im, folder)
        os.mkdir(sub_final)
        # now we are ready to merge images
        # have to figure out what method to use
        if(generate_background):
            #for file in os.listdir(sub_obj):

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
            mi.generate_for_all_objects(sub_obj,backgr_dat ,sub_final)



    # currently we zip the object poses, but once we have the actual
    # training images, it is easy to just change the name

    for folder in os.listdir(obj_poses):
        print(folder)

    # export everything into a zip file
    make_archive(zip_name, 'zip',final_folder)

    #input("press enter to continue")
    destroy_folders(work_dir, temp_folders)



#full_run(zip_save, generate_background = True, backgr_dat = backg_database)

blender_attributes = {
    "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
    "attribute_distribution" : []
}

#blender_attributes ={}

"""zip name"""
zip_save1 = os.path.join(workspace, "final_zip/sun_data")
zip_save2 = os.path.join(workspace, "final_zip/random_data")
backg_database = os.path.join(workspace,"bg_database/SUN_back/")
obj_set = os.path.join(workspace, "object_files/two_set")
bl_path = "E:\Blender_Foundation\Blender\\blender"
"""working_directory"""
argument_list = []
arguments1 = {"zip_name": zip_save1, "obj_set": obj_set ,"blender_path": bl_path,"renders_per_class": 2,"work_dir": workspace, "generate_background": False, "backgr_dat": backg_database, "blender_attributes": blender_attributes}
arguments2 = {"zip_name": zip_save2, "obj_set": obj_set ,"blender_path": bl_path,"renders_per_class": 2,"work_dir": workspace, "generate_background": True, "backgr_dat": backg_database, "blender_attributes": blender_attributes}
#argument_list.append(arguments1)
argument_list.append(arguments2)

for value in argument_list:
    full_run(**value)
    print("One run done")

    