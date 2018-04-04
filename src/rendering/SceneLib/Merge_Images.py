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
import time
import numpy as np

Image_height = 360
Image_width = 360
base_address= "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/data/"
SUN_images_dir = "E:/LabelMeToolbox/real_data/images/"
#final_address = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/images/resized_background/"


def add_background(foreground_name, background_name, save_as, adjust_brightness = False):
    """
    Function that give an RGBA and any image file merges them into one.
    
    Args:
        foregroun_name (string): The name of the RGBA image
        background_name (string): Name of the background image
        save_as (string): Name under which the final image is to be saved
        adjust_brigthness (boolean): If the adjust brightness algorithm should be used
    """
    try:
        foreground=Image.open(foreground_name)
    except:
        print("Invalid foreground images, skipping", foreground_name)
        return "ForegroundError"   
    try:
        background=Image.open(background_name)
    except:
        #This is technically problematic as we might throw away
        # valid object poses because of invalid backgrounds
        print("Invalid background image skipping", background_name)
        return "BackgroundError" 
    
    background.paste(foreground, (0, 0), foreground)
    background.save("tested2.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    
    
    if adjust_brightness:
        
        for_array = np.array(foreground)
        
        """
        frgdnumber = 0
        frgdsum = 0
        
        for one_tuple in list(foreground.getdata()):
            if(one_tuple[3]>0):
                frgdnumber +=1
                frgdsum += sum(one_tuple[0:3])
        """        
        frgdnumber = np.count_nonzero(np.count_nonzero(for_array, axis=2))
        frgdsum = np.sum(np.sum(np.sum(for_array, axis=0), axis=0)[0:3])
        
        """
        bcgdnumber = 0
        bcgdsum = 0
        for one_tuple in list(background.getdata()):
            bcgdnumber +=1
            bcgdsum += sum(one_tuple)
        """    
        
        bc_size = background.size
        back_array = np.array(background)
        
        bcgdnumber = bc_size[0]*bc_size[1]#np.count_nonzero(np.count_nonzero(back_array, axis=2))
        bcgdsum = np.sum(np.sum(np.sum(back_array, axis=0), axis=0))

        frmean = frgdsum/frgdnumber
        bcmean = bcgdsum/bcgdnumber 
        factor = frmean/bcmean

        #print(factor)
        # Imposing boundaries on the factor
        factor = min(factor, 1.5)
        factor = max(factor, 0.5)
        #print(factor)
        back_array = back_array*factor
        back_array[back_array>255]=255
        #back_array = np.minimum(back_array,255)
        background = Image.fromarray(np.uint8(back_array))
        """
        for i in range(bc_size[0]):    # for every col:
            for j in range(bc_size[1]):    # For every row
                background_new[i,j] = tuple([int(factor*x) for x in background_new[i,j]])
        """        

    background.paste(foreground, (0, 0), foreground)
    background.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)


def merge_images(foreground, background):
    """                          
    Merges two images. The difference is that this accepts Images as input
    not path to the image
    """
    
    background.paste(foreground, (0, 0), foreground)
    return background
               
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

    all_backgrounds = os.listdir(background_folder)
    for object_image in os.listdir(objects_folder):
        one_object = random.choice(all_backgrounds)
        just_name = os.path.splitext(object_image)[0]
        add_background(objects_folder+"/"+object_image, background_folder+"/"+one_object, final_folder+"/"+just_name+".jpg", True)
        
if __name__ == "__main__":
    start_time = time.time()
    generate_for_all_objects(base_address+"object_poses/test", base_address+"resized_background/test", base_address+"test_results")
    print("--- %s seconds ---" % (time.time() - start_time))
    #generate_for_all_objects(base_address+"object_poses/Halloumi_white", base_address+"resized_background/white_back", base_address+"final_images/white/halloumi/train")