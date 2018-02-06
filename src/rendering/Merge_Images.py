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
SUN_images_dir = "E:/LabelMeToolbox/real_data/images/"
resized_address = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/images/resized_backgrounds/"


def add_background(foreground_name, background_name, save_as):
    
    foreground = Image.open(foreground_name)
    background = Image.open(background_name)

    background.paste(foreground, (0, 0), foreground)
    #background.show()
    background.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
    

# This is the prototype that is being used in the actual resizing function
def resize_and_crop(image_address, output_address):
    with open(image_address, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [Image_width, Image_height])
            cover.save(output_address, image.format)
"""           
#This function is not used at the moment
# as we need the final image to be a square shape
# so we need cropping            
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
            if(width>=height and height>Image_height):
                cover = resizeimage.resize_height(image, Image_height)
            elif (height>width and width> Image_width):
                cover = resizeimage.resize_width(image, Image_width)
            else:
                cover = image
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
"""
            
def generate_for_all_objects(objects_folder, background_folder, final_folder):
    # Generates the final images for each object pose to which 
    # a random background is merged
    all_backgrounds = os.listdir(base_address+background_folder)
    for object_image in os.listdir(base_address+objects_folder):
        one_object = random.choice(all_backgrounds)
        add_background(base_address+objects_folder+"/"+object_image, base_address+background_folder+"/"+one_object, base_address+final_folder+"/"+object_image)
        
        

"""
# Older function that tried to manually iterate through the directories
# See resize_all_files for the new version
# For now leaving the function here
def filter_and_resize(min_pixels):
    #For each image in each folder in each folder 
    # (e.g. folder 'a'-> 'attic'->image.jpg) we check 
    # if image is large enough (given parameters)
    # if yes, we rescale it to given size and save in resized_address
    count = 0
    for letter_folder in os.listdir(SUN_images_dir):
        subfolder_name = SUN_images_dir+letter_folder+"/"
        for category in os.listdir(subfolder_name):
            category_name = subfolder_name+category+"/"
            for image_name in os.listdir(category_name):
                with Image.open(category_name+image_name) as tested_image:
                    width, height = tested_image.size
                    if(width>=min_pixels and height>= min_pixels):                        
                        cover = resizeimage.resize_cover(tested_image, [min_pixels, min_pixels])
                        cover.save(resized_address+image_name, 'JPEG')
                    
                    count +=1    
                    if(count>=100):
                        return
"""                       

# This function takes all images of the SUN database, resize them to given
# shape and saves them to a given folder
# it seems to be able to find its way through all levevls of directories
# This will be a one of to generate the database of resized images
def find_all_files(min_pixels):
    count = 0
    for root, dirs, files in os.walk(SUN_images_dir):
        print(root)
        print(dirs)
        print(files)
        if(len(files)>0):
            for image_name in files:
                with Image.open(root+"/"+ image_name) as tested_image:
                        width, height = tested_image.size
                        if(width>=min_pixels and height>= min_pixels):                        
                            cover = resizeimage.resize_cover(tested_image, [min_pixels, min_pixels])
                            cover.save(resized_address+image_name, 'JPEG')
        # the below condiion is for testing
        # so that it does not run over the entire folder
        # in the end it will be removed
        count +=1
        if(count>5):
            return 
    return 

#find_all_files(360)

#just_resize("cup_image.jpg", base_address + "/resized_images/test-resized.jpeg")
#rescale_all("background_images", "resized_background")
generate_for_all_objects("object_poses", "resized_background", "final_images")

#resize_and_crop("cup_image.jpg", "test-cropped.jpeg")
#add_background("render50.png","test-cropped.jpeg")