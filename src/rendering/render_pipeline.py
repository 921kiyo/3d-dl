# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:51:48 2018

@author: Pavel

Run on commmand line using this command
blender --background --python render_pipeline.py

"""

import sys
import random
#import math
#import bpy
#import csv
import os


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
#    
##import src.rendering.RandomLib.random_background as rb
#import src.rendering.SceneLib.Merge_Images as MI
#
#if(os.path.isdir(workspace) is False):
#    print("Could not find workspace directory")
#    
#def create_workspace(workspace, gener_back = True):
#    """
#    This function will be called at the begining of any execution
#    It will prepare all necessary folders for the execution
#    It will check if it needs to generate its own
#    """
#
#def generate_poses(obj_folder, output_folder, n_of_poses):
#    """
#    This will generate poses for a given class, and save it to a given folder
#    """
#    return
#
#def generate_random_background(folder, number):
#    return
#
#
#def clean_up():
#    return    
#

import argparse
import subprocess
from shutil import rmtree, make_archive
from PIL import Image
import numpy as np

#import random
import src.rendering.SceneLib.Merge_Images as mi
import src.rendering.RandomLib.random_background as rb

""" --------------- CLI setup ------------- """
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

""" --------------- Setup and configuration ------------- """
# path to blender library

#import BlenderAPI as bld

# GPU rendering
#if args.gpu:
#    C = bpy.context
#    C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
#    C.user_preferences.addons['cycles'].preferences.devices[0].use = True
#    C.scene.render.engine = 'CYCLES'


"""------------ Validate data path and content folders ----------- """

data_folders = ['object_files',
                'bg_database',
                'generate_bg',
                'object_poses',
                'final_folder',
                'final_folder/images',
                'final_zip']

temp_folders = ['generate_bg',
                #'object_poses', #  for testing, otherwise uncomment
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
    diff = list(set(folder_list) - set(os.listdir(target_folder)))
    print(os.listdir(target_folder))
    if not diff == []:
            for folder in diff:
                os.mkdir(os.path.join(target_folder,folder))

def destroy_folders(target_folder, folder_list):
    for folder in folder_list:
        full_path = os.path.join(target_folder,folder)
        if(os.path.isdir(full_path)):
            rmtree(full_path)
            
def generate_poses():
    """
    This function will call Blender to Generate object poses
    Wait for Max
    """
    return

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
    final.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)

def full_run(zip_name, work_dir = workspace, generate_background = True, backgr_dat = None ):
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

    
    """
    code to generate object poses
    """
    
    """------------------------Code to generate final images----------"""
    """ 
    We need to distinguish between the case of drawing backrounds
    from a database and when generating ourselves
    """
    obj_poses = os.path.join(work_dir, "object_poses")
    final_folder = os.path.join(work_dir, "final_folder")
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
                try:
                    path = os.path.join(sub_obj, image)
                    print(path)
                    foreground=Image.open(path)
                    
                    
                    just_name = os.path.splitext(image)[0]
                    name_jpg = just_name+".jpg"
                    save_to = os.path.join(sub_final, name_jpg)
                    gen_merge(foreground, save_to, pixels = 300)
                    print(just_name)
            
                    # do stuff
                except IOError:                
                    print("skipping", image)
                    continue
            print("Here I will generate background")
        elif(generate_background is False and backgr_dat is None):
            print("We need a background database")
            return
        else:
            mi.generate_for_all_objects(sub_obj,backgr_dat ,sub_final)
            
        
    
    # currently we zip the object poses, but once we have the actual
    # training images, it is easy to just change the name
    
    for folder in os.listdir(obj_poses):
        print(folder)
        

    
    make_archive(zip_name, 'zip',final_folder)

    input("press enter to continue")
    destroy_folders(work_dir, temp_folders)

zip_save = os.path.join(workspace, "final_zip/test1")
backg_database = os.path.join(workspace,"bg_database/SUN_back/")
full_run(zip_save, generate_background = True, backgr_dat = backg_database)
#print('Changed working directory to {}\n'.format(os.getcwd()))


""" --------------- Render product images from models --------------- """

#
#def find_files(product_folder):
#    """Naively return name of object and texture file in a folder"""
#    # TODO add more sophisticated checking once format of object files concrete
#    object_file = ''
#    texture_file = ''
#
#    files = os.listdir('objects')
#
#    for file in files:
#        if file.endswith('.obj'):
#            object_file = file
#        elif file.endswith('.jpg'):
#            texture_file = file
#
#    return object_file, texture_file


def render_images(renders_per_product, data_folder):
    """"Generate object renders and save to renders folder"""
    blender_args = ['blender', '--background', '--python', 'render_images.py', '--',
                    data_folder,
                    str(renders_per_product)]

    subprocess.check_call(blender_args)

#if args.render:
#    print('Rendering {} images per product'.format(args.render))
#    render_images(args.render)


""" --------------- Merge renders and backgrounds to create final images --------------- """


def merge_images():
    """Merge each pose with a random background images and save to final images folder"""

    all_backgrounds = os.listdir('resized_background')

    for object_folder in os.listdir('object_poses'):
        if not os.path.isdir(os.path.join('object_poses', object_folder)):
            continue

        print("Merging renders in folder", object_folder)
        for object_image in os.listdir(os.path.join('object_poses', object_folder)):
            if not object_image.endswith('.png'):
                continue

            while True:
                background = random.choice(all_backgrounds)
                if background.endswith('.jpeg'):
                    break

            add_background(os.path.join('object_poses', object_folder, object_image),
                           os.path.join('resized_background', background),
                           os.path.join('final_images', object_folder + '-' + object_image))

#
#if args.merge:
#    print('Merging each pose with a random background images')
#    merge_images()

