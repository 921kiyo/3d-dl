# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:51:48 2018

@author: Pavel

Run on commmand line using this command
blender --background --python render_pipeline.py

"""

import sys
import random
import math
import bpy
import csv
import os


# set use GPU
"""
C = bpy.context
C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
C.user_preferences.addons['cycles'].preferences.devices[0].use = True
C.scene.render.engine = 'CYCLES'
"""
# path to blender library

boop = 'D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/src/rendering/BlenderAPI'
# above is for Pavel so he does not have to set it every time
#boop = 'D:/PycharmProjects/Lobster/src/'
#boop = '/vol/bitbucket/who11/CO-530/Lobster/src'
dir_path = os.path.dirname(os.path.realpath(__file__)) # the src folder
rend_folder = os.path.abspath(os.path.join(dir_path, os.pardir))
ocado_folder = os.path.abspath(os.path.join(rend_folder,os.pardir))
workspace  = os.path.join(ocado_folder, "render_workspace")

if not (ocado_folder in sys.path):
    sys.path.append(ocado_folder)
    
    
sys.path.append("E:/Blender_Foundation/Blender/2.79/python/lib/site-packages/")
sys.path.append("E:/Anaconda/Lib/site-packages/scipy/")
    
#import src.rendering.RandomLib.random_background as rb
import src.rendering.SceneLib.Merge_Images as MI

if(os.path.isdir(workspace) is False):
    print("Could not find workspace directory")
    
def create_workspace(workspace):
    """
    This function will be called at the begining of any execution
    """

def generate_poses(obj_folder, output_folder, n_of_poses):
    """
    This will generate poses for a given class, and save it to a given folder
    """
    return

def generate_random_background(folder, number):
    return


def clean_up():
    return    

 

print(ocado_folder)