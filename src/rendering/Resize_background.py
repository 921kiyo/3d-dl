# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:01:13 2018

@author: Pavel
"""

"""
This function will take the whole of SUN database and flaten it into a single 

"""
import os
from PIL import Image
from resizeimage import resizeimage

#the below should point to the file containing the alphabet letter folders
SUN_images_dir = "E:/LabelMeToolbox/real_data/images/"
resized_address = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/images/resized_backgrounds/"


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
                        

def find_all_files(min_pixels):
    count = 0
    for root, dirs, files in os.walk(SUN_images_dir):
        print(root)
        print(dirs)
        print(files)
        if(len(files)>0):
            print(files[0])
            for image_name in files:
                with Image.open(root+"/"+ image_name) as tested_image:
                        width, height = tested_image.size
                        if(width>=min_pixels and height>= min_pixels):                        
                            cover = resizeimage.resize_cover(tested_image, [min_pixels, min_pixels])
                            cover.save(resized_address+image_name, 'JPEG')
           
        count +=1
        if(count>5):
            return files
    return files

roots= find_all_files(360)

                        
#filter_and_resize(360)                        
                        
                    