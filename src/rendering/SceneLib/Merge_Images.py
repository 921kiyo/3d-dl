# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:40:33 2018

@author: Pavel

This file includes functionality for combination of object poses with 
background images. It also allows for the object to be translated first.
During merging the brightness of the background can be adjusted to match
that of the object pose.

"""
import os
import random
from PIL import Image
import time
import numpy as np
from resizeimage import resizeimage

Image_height = 360
Image_width = 360
base_address= "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/data/"
SUN_images_dir = "E:/LabelMeToolbox/real_data/images/"
#final_address = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/images/resized_background/"

class ImageError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


def add_random_offset_foreground(foreground_image, pad_ratio=0.0):
    """
    Function that adds a translation to the object pose, before merging
    with the background. An occlusion is also introduced by allowing part
    of the object to move outside of the image frame. This leads to only part
    of the object being visible in the final image. The amount of possible
    occlusion is controlled by the pad_ratio. A temporary frame is created
    that is larger on each side than the original image by 
    original_dim*pad_ratio. E.g. 300*300 pixel image with pad_ratio 0.1
    will create a 320*320 frame. The object is then moved to a random position
    within this frame. A final image is created by taking the original sized
    image, cutting out any part of the object being outside of this image. 

    Arguments:
        foreground_image (PIL image): An object pose to be translated
        pad_ratio (float): Additional padding around the original image.
                        Introduced for the purpose of occlusion. See above.
                        
    Returns:
        Translated Image (PIL image):
        A object bounding box coordinates (tuple): (x0,x1),(y0,y1)
    """

    # extract subject square
    size = foreground_image.size
    fg_arr = np.array(foreground_image)
    R, C = np.nonzero(fg_arr[:,:,3])
    y0 = np.min(R)
    y1 = np.max(R)
    x0 = np.min(C)
    x1 = np.max(C)
    subject_square = fg_arr[y0:y1+1,x0:x1+1,:]

    # determine range of motion
    padding = (int(np.round(pad_ratio*size[0])), int(np.round(pad_ratio*size[1])))
    padded_size = (size[0] + 2*padding[0], size[1]  + 2*padding[1])
    w = x1 - x0
    h = y1 - y0
    dw_max = padded_size[1] - w
    dh_max = padded_size[0] - h
    dw = np.random.randint(0, dw_max)
    dh = np.random.randint(0, dh_max)

    fg_arr_pad = np.zeros(shape=(padded_size[0], padded_size[1], 4), dtype=fg_arr.dtype)
    # compute the foreground bb's in the padded image
    x0_pad = dw
    x1_pad = w + dw + 1
    y0_pad = dh
    y1_pad = h + dh + 1
    fg_arr_pad[y0_pad:y1_pad, x0_pad:x1_pad, :] = subject_square
    fg_arr_new = fg_arr_pad[padding[0]:(padding[0]+size[0]), padding[1]:(padding[1]+size[1]),:]

    # compute the new foreground bb's
    x0_new = min(max(0, x0_pad-padding[0]), size[0]-1)
    x1_new = min(max(0, x1_pad-padding[0]), size[0]-1)
    y0_new = min(max(0, y0_pad-padding[1]), size[1]-1)
    y1_new = min(max(0, y1_pad-padding[1]), size[1]-1)

    return Image.fromarray(fg_arr_new), ((x0_new,x1_new),(y0_new,y1_new))

def add_background(foreground_name, background_name, save_as, adjust_brightness = False, n_of_pixels = 300):
    """
    Function that give an RGBA and any image file merges them into one.
    It ensures that the final image is of the specified size. 
    If either of the given images is too small, an error is returned.
    The brightness of the background can be adjusted to be better
    correspond to the brightness of the foreground. This is optional
    functionality that is triggered by the corresponding input parameter.
    
    Args:
        foregroun_name (string): The name of the RGBA image
        background_name (string): Name of the background image
        save_as (string): Complete path with name under which the final image 
            is to be saved
        adjust_brigtness (boolean): Whether the brigthness of the background
            should be adjusted to match on average the brightness of the 
            foreground image. Default = False
            
    Return:
        bbox (integer tuple): (x0,x1),(y0,y1) the bounding box around the 
                    foreground object .
    """
    try:
        foreground=Image.open(foreground_name)
        foreground, bbox = add_random_offset_foreground(foreground, pad_ratio=0.1)
    except:
        print("Invalid foreground images, skipping", foreground_name)
        raise ImageError(("Invalid foreground images, skipping", foreground_name))   
    try:
        background=Image.open(background_name)
    except:
        #This is technically problematic as we might throw away
        # valid object poses because of invalid backgrounds
        print("Invalid background image skipping", background_name)
        raise ImageError(("Invalid background image skipping", background_name))
    
    bc_size = background.size
    if(n_of_pixels > bc_size[0] or n_of_pixels > bc_size[1]):
        print("Background too small to be resized") 
        raise ImageError("Background too small to be resized")
                
    elif(n_of_pixels < bc_size[0] or n_of_pixels < bc_size[1]):
        background = resizeimage.resize_cover(background, [n_of_pixels, n_of_pixels])
    #else means it has exactly the correct size, do nothing   
    
    fg_size = foreground.size
    
    if(n_of_pixels != fg_size[0] or n_of_pixels != fg_size[1]):
        print("Resolution of the object pose given does not match the given number of pixels") 
        raise ImageError("Resolution of the object pose given does not match the given number of pixels")
    
    
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
        
        #bc_size = background.size
        back_array = np.array(background)
        
        bcgdnumber = bc_size[0]*bc_size[1]#np.count_nonzero(np.count_nonzero(back_array, axis=2))
        bcgdsum = np.sum(np.sum(np.sum(back_array, axis=0), axis=0))

        frmean = frgdsum/frgdnumber
        bcmean = bcgdsum/bcgdnumber 
        factor = frmean/bcmean

        # Imposing boundaries on the factor
        factor = min(factor, 1.5)
        factor = max(factor, 0.5)

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
    return bbox


def merge_images(foreground, background):
    """                          
    Merges two PIL images. 
    Arguments:
        foreground (PIL image): Foreground image. It is necessary for this 
                image to have alpha channel so that the background is visible
        background (PIL image): Image to be used as background. 
                Does not have to have alpha channel
                
    Return:
        background (PIL image): Final merged image
        bbox (integer tuple): (x0,x1),(y0,y1) the bounding box around the 
                    foreground object .
    """
    foreground, bbox = add_random_offset_foreground(foreground, pad_ratio=0.1)
    background.paste(foreground, (0, 0), foreground)
    return background, bbox
               
def generate_for_all_objects(objects_folder, background_folder, final_folder, adjust_brightness = False, n_of_pixels = 300):
    """
    This function takes every image in objects_folder, merge it
    with a random image from background_folder and saves it in final_folder.
    It works for any images sizes but for consistency of scale it is
    advised to rescale the images
    
    Args:
        objects_folder (string): Folder containing the foreground RGBA images
        background_folder (string): Folder containg background images
        final_folder (string): Folder to which save the final images
        
    Return:
        all_bbox (Dictionary): Dictionary of bounding boxes (x0,x1),(y0,y1) 
            around the object. The name of the final image is used as a key in
            the dictionary.
        
    """

    all_backgrounds = os.listdir(background_folder)
    all_bbox = {}
    for object_image in os.listdir(objects_folder):
        one_object = random.choice(all_backgrounds)
        just_name = os.path.splitext(object_image)[0]
        try:
            bbox = add_background(objects_folder+"/"+object_image, background_folder+"/"+one_object, final_folder+"/"+just_name+".jpg", adjust_brightness, n_of_pixels)
            all_bbox[just_name+".jpg"] = bbox
        except Exception as e:
            print("The following error occured during background addition:", e)
            raise e

    return all_bbox
            
        
if __name__ == "__main__":
    #start_time = time.time()
    generate_for_all_objects(base_address+"object_poses/test", base_address+"resized_background/test", base_address+"test_results", n_of_pixels = 300)
    
    #generate_for_all_objects(base_address+"object_poses/Halloumi_white", base_address+"resized_background/SUN_back", base_address+"final_images/sun/halloumi/train", True)
    #print("--- %s seconds ---" % (time.time() - start_time))