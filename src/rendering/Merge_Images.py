# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:40:33 2018

@author: Pavel
"""
import os
import random
from PIL import Image
from resizeimage import resizeimage



Image_height = 360
Image_width = 360
base_address= "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/data/"

def add_background(foreground_name, background_name, save_as):
    
    foreground = Image.open(foreground_name)
    background = Image.open(background_name)

    background.paste(foreground, (0, 0), foreground)
    #background.show()
    background.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
    

def resize_and_crop(image_address, output_address):
    with open(image_address, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [Image_width, Image_height])
            cover.save(output_address, image.format)
            
def just_resize(image_address, output_address):
    #This keeps the original ratio of the resized image
    # It rescales it, so that it smaller side has the same size  
    # as the size of the Object image
    # Carefull! this function assumes that the object image
    # is approximatly square
    # If it does not hold, it is safer to use resize_and_crop 
    with open(image_address, 'r+b') as f:
        with Image.open(f) as image:
            width, height = image.size
            if(width>=height):
                cover = resizeimage.resize_height(image, Image_height)
            else:
                cover = resizeimage.resize_width(image, Image_width)
            cover.save(output_address, image.format)
                        
            
def each_in_folder(foldername):
    # Skeleton for any function that iterates over all files in folder
    for filename in os.listdir(foldername):
        
        foo(filename)
    
    
def rescale_all(original_folder, final_folder):
    # rescale all backgrounds so that its smaller size is equal to 
    # the size of the object pose
    full_folder_path = base_address + original_folder + "/"
    for filename in os.listdir(full_folder_path):
        just_resize(full_folder_path+filename, base_address + final_folder+"/"+os.path.splitext(filename)[0]+"_resize.jpeg")
            
def generate_for_all_objects(objects_folder, background_folder, final_folder):
    # Generates the final images for each object pose to which 
    # a random background is merged
    all_backgrounds = os.listdir(base_address+background_folder)
    for object_image in os.listdir(base_address+objects_folder):
        one_object = random.choice(all_backgrounds)
        add_background(base_address+objects_folder+"/"+object_image, base_address+background_folder+"/"+one_object, base_address+final_folder+"/"+object_image)

#just_resize("cup_image.jpg", base_address + "/resized_images/test-resized.jpeg")
rescale_all("background_images", "resized_background")
generate_for_all_objects("object_poses", "resized_background", "final_images")

#resize_and_crop("cup_image.jpg", "test-cropped.jpeg")
#add_background("render50.png","test-cropped.jpeg")