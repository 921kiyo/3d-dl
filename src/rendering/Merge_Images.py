# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:40:33 2018

@author: Pavel

This file includes functionality for combination of object poses with 
background images.

"""
import os
import random
from PIL import Image

Image_height = 360
Image_width = 360
base_address= "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/data/"
SUN_images_dir = "E:/LabelMeToolbox/real_data/images/"
resized_address = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/images/resized_backgrounds/"


def add_background(foreground_name, background_name, save_as):
    """
    Function that give an RGBA and any image file merges them into one.
    
    Args:
        foregroun_name (string): The name of the RGBA image
        background_name (string): Name of the background image
        save_as (string): Name under which the final image is to be saved
    """    
    foreground = Image.open(foreground_name)
    background = Image.open(background_name)

    background.paste(foreground, (0, 0), foreground)
    background.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
                          
               
def generate_for_all_objects(objects_folder, background_folder, final_folder):
    """
    This function takes every image in objects_folder, merge it
    with a random image from background_folder and saves it in final_folder.
    It works for any images sizes but for consistency of scale it is
    advised to rescale the images
    
    Args:
        objects_folder (string): Folder containing the foreground RGBA images
        background_folder (string): Folder containg background images
        final_folder (string): Folder to which save the final images
        
    Returns:
        Nothing
    """
    all_backgrounds = os.listdir(base_address+background_folder)
    for object_image in os.listdir(base_address+objects_folder):
        one_object = random.choice(all_backgrounds)
        add_background(base_address+objects_folder+"/"+object_image, base_address+background_folder+"/"+one_object, base_address+final_folder+"/"+object_image)
        
        

generate_for_all_objects("object_poses", "resized_background", "final_images")