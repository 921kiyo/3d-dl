# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:51:48 2018

@author: Pavel

Rendering Pipeline. This file contains all necessary calling functions
for full rendering from object files to final images zip file.

The calls for running the script can be found in bottom part of the code.
Two dictionaries of parameters are necessary. One contains the parameters
for Blender and one contains the parameters for Merging.

For more detailed description and example see the appropriate function
and an example at the end of file.

Run on commmand line using this command from parent directory src
python -m rendering.render_pipeline

"""

import sys
from shutil import rmtree, make_archive
from shutil import move as sh_move
from PIL import Image
import numpy as np
import os
import subprocess
import json
import datetime
import time

"""
Here the paths have to be set up.

The file require other modules from the src folder,
the project_path should point to the folder that contains the src

The rendering process requires obj files and other images.
These should be in render_workspace.
A functioning render_workspace is in the group folder, but feel free
to download it using psftp and place it on your system.
Do not forget to change the path to render_workspace as it is hard coded.

"""
#boop = '/vol/bitbucket/who11/CO-530/Lobster/src'

# Ensure source files are in python path
rendering_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.abspath(os.path.join(rendering_path, os.pardir))
project_path = os.path.abspath(os.path.join(src_path, os.pardir))
#project_path = '/vol/bitbucket/who11/CO-530/Lobster/'
workspace = os.path.join(project_path, "render_workspace")
#workspace = '/vol/project/2017/530/g1753002/render_workspace'
# workspace = '/Users/maxbaylis/Desktop/render_workspace'

# Set Blender path
bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
#bl_path = "E:\Blender_Foundation\Blender\\blender" # for Pavel
# bl_path = "blender" # for Max

if not project_path in sys.path:
    sys.path.append(project_path)

if not src_path in sys.path:
    sys.path.append(src_path)


from .SceneLib import Merge_Images as mi
from .RandomLib import random_background as rb

"""------------ Create Slack reporter ----------- """
from . import SlackReporter
# to disable sending messages pass disable=True to constructor
slack = SlackReporter.SlackReporter(disable=True)


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

class RenderPipelineError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

def validate_folders(target_folder, folder_list):
    """
    Check whether all folders in folder_list are present in the target_folder
    If not, create them.
    :param target_folder: path to the folder in which to create subfolders
    :param folder_list: list of strings, giving the names of folders that
            must be present in the target_folder
    """
    diff = sorted(list(set(folder_list) - set(os.listdir(target_folder))))
    print("Creating the following folders: ", sorted(diff))
    if not diff == []:
            for folder in diff:
                print("making ", folder)
                os.mkdir(os.path.join(target_folder, folder))


def destroy_folders(target_folder, folder_list):
    """
    Destroy all folders in the target folder that are on the folder list
    :param target_folder: path to folder in which to delete subfolders
    :param folder_list: list of folder names to delete
    """
    for folder in folder_list:
        full_path = os.path.join(target_folder, folder)
        if(os.path.isdir(full_path)):
            rmtree(full_path)


"""------------ Helper functions ----------- """
def generate_poses(src_dir, blender_path, object_folder, output_folder, renders_per_product, blender_attributes, visualize_dump=False, dry_run_mode=False, render_resolution=300, render_samples=128):
    """
    Make a system call to Blender, passing the configuration for this run
    and wait for Blender to return.

    args:
        src_dir: full path to project source code, so Blender can add to its path
        blender_path: path to the Blender executable
        object_folder: path to a folder containing folders of .obj files
        output_folder: path to which Blender should save the rendered images
        renders_per_product: number of images to generate per product (.obj file)
        blender_attributes: a dictionary of Blender configurations.

    Passing Rendering Parameters to Blender:
        Rendering parameters should be passed to Blender in a dictionary of the format

        blender_attributes = {
            "attribute_distribution_params": list(list[string, string, float]),
            "attribute_distribution" : list(list(string, dict(string, float, float)))
        }

        Only one of attribute_distribution_params or attribute_distribution
        should be set for each run. Leave the unused element as an empty list.

        Examples:
        "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]]

        "attribute_distribution" : [["lamp_energy", {"dist":"UniformD","l":2000.0,"r":2400.0}]]

        blender_attributes = {
            "attribute_distribution_params": [["num_lamps","l", 5], ["num_lamps","r", 8], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
            "attribute_distribution" : []
        }
    """
    print("Project source dir is", src_dir)
    print("Blender path is ", blender_path)

    blender_script_path = os.path.join(src_dir, 'rendering', 'render_poses.py')
    blender_args = [blender_path, '--background', '--python-exit-code', '2','--python', blender_script_path, '--',
                    src_dir,
                    object_folder,
                    output_folder,
                    str(renders_per_product),
                    str(render_resolution),
                    str(render_samples),
                    json.dumps(blender_attributes),
                    str(visualize_dump),
                    str(dry_run_mode)]

    print('\n')
    print(' ============================ LAUNCHING BLENDER FOR POSE RENDERING ============================')
    print('\n')
    try:
        subprocess.check_call(blender_args)
    except subprocess.CalledProcessError as e:
        raise RenderPipelineError("Error during pose generation! The returned subprocess error code is : {}".format(e.returncode))
    print('\n')
    print(' ============================ CLOSING BLENDER FOR POSE RENDERING ============================')
    print('\n')


def gen_merge(image, save_as, pixels=300, adjust_brightness = False):
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
        adjust_brigtness (boolean): Whether the brigthness of the background
            should be adjusted to match on average the brightness of the
            foreground image. Default = False

    returns:
        bbox - bounding box information around the object after translation
    """

    back = rb.rand_background(np.random.randint(2,4),pixels)
    scaled = back*256

    if adjust_brightness:
        for_array = np.array(image)
        frgdnumber = np.count_nonzero(np.count_nonzero(for_array, axis=2))
        frgdsum = np.sum(np.sum(np.sum(for_array, axis=0), axis=0)[0:3])

        bcgdnumber = pixels*pixels#np.count_nonzero(np.count_nonzero(back_array, axis=2))
        bcgdsum = np.sum(np.sum(np.sum(scaled, axis=0), axis=0))

        frmean = frgdsum/frgdnumber
        bcmean = bcgdsum/bcgdnumber
        factor = frmean/bcmean
        # Imposing boundaries on the factor
        factor = min(factor, 1.5)
        factor = max(factor, 0.5)

        scaled = scaled*factor
        scaled[scaled>255]=255

    background = Image.fromarray(scaled.astype('uint8'), mode = "RGB")
    final, bbox = mi.merge_images(image, background)

    try:
        final.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
        return bbox
    except Exception as e:
        #slack.send_message('Error in gen_merge. Output file: ' + save_as, 'Rendering Error', 'warning')
        raise RenderPipelineError("Error during image merging!")

def random_bg_for_all_objects(objects_folder, final_folder, adjust_brightness = False, n_of_pixels = 300):
    """
    Provides interface for gen_merge for large number of images.
    For each object pose (image) in objects_folder, generates a random colour
    mesh background, merge the images and save the final image into
    final_folder.
    args:
        objects_folder (string): path to folder containing object poses
        final_folder (string): path to destination folder for the final images
        adjust_brightness (bool): If the background brightness should be
                adjusted to match the foreground brightness
        n_ox_pixels (int): the size of one side of the final square image.
    returns:
        bboxes: Dictionary of bounding boxes for each object
    """
    bboxes = {}
    # for each object pose
    for image in os.listdir(objects_folder):
        path = os.path.join(objects_folder, image)
        try:
            foreground = Image.open(path)
        except:
            print("skipping", image)
            continue

        just_name = os.path.splitext(image)[0]
        name_jpg = just_name + ".jpg"
        save_to = os.path.join(final_folder, name_jpg)
        bbox = gen_merge(foreground, save_to, n_of_pixels, adjust_brightness)
        bboxes[name_jpg] = bbox
        foreground.close()

    return bboxes

def full_run( obj_set, blender_path, renders_per_class=10, work_dir=workspace, generate_background=True, background_database=None, blender_attributes={}, visualize_dump=False, dry_run_mode=False, n_of_pixels = 300, adjust_brightness =False, render_samples=128):
    """
    Function that will take all the parameters and execute the
    complete pipeline. Given object model files it will generate the specified
    number of training images and save them in a zip file format.
    At the end of the run, this function will clean up all files created,
    apart from the final zip file. This is due to the fact that large number
    of images is produced which would require large amounts of storage space.

    args:
        obj_set: Path to the folder containing folders with individual
                model object files
        blender_path: path to the blender executable
        renders_per_class: number of images to be generated per class.
                Default = 10
        work_dir: path to the workspace that contains individual folders
        generate_background: Flag, if True, we will generate random background
                if False, will use images in a given database. Default =True
        background_database: Path to databse of backgrounds to use if
                generate_background is False
        blender_attributes: A dictionary containing attributes for blender.
                Optional parameter, if none given, basic predefined attributes
                will be used. Default = {}
        visualize_dump:
                Default = False
        dry_run_mode:
                Default = False
        n_of_pixels (int): The size of the edge of the square image.
                Is optional, Default = 300
        adjust_brigtness (boolean): Whether the brigthness of the background
                should be adjusted to match on average the brightness of the
                foreground image. Default = False
        render_samples:
                Default = 128
    """
    print('Checking data directories...')
    slack.send_message('Obj_set: ' + obj_set + '\n renders_per_class: ' + str(renders_per_class), 'Rendering Run Started', 'good')

    # Ensure render_workspace folder exists
    if not os.path.isdir(work_dir):
        message = "Can't find rendering workspace folder. Please create the folder " + work_dir +  ", containing object files and background database. See group folder for example."
        print(message)
        raise RenderPipelineError(message)

    destroy_folders(work_dir, temp_folders)
    validate_folders(work_dir, data_folders)

    obj_poses = os.path.join(work_dir, "object_poses")

    """----------------- Generating object poses ---------------"""
    src_path = os.path.join(project_path, "src")
    generate_poses(src_path, blender_path, obj_set, obj_poses, renders_per_class, blender_attributes, visualize_dump, dry_run_mode, n_of_pixels, render_samples)

    #now we need to take Ong' stats and move them into final folder
    for folder in os.listdir(obj_poses):
        orig_stats=os.path.join(obj_poses,folder,"stats")

        if(os.path.isdir(orig_stats)):
            final_name= folder + "_stats"
            sh_move(orig_stats, os.path.join(work_dir,"final_folder" ,final_name))

    """----------------- Generating final images ---------------"""
    """
    We need to distinguish between the case of drawing backrounds
    from a database and when generating ourselves
    """
    print(' ============================ GENERATING FINAL IMAGES ============================')
    final_folder = os.path.join(work_dir, "final_folder")
    final_im = os.path.join(work_dir, "final_folder/images")
    all_bbox = {}
    # Generate images for each class poses
    for folder in os.listdir(obj_poses):
        sub_obj = os.path.join(obj_poses, folder)
        if os.path.isdir(sub_obj) is False:
            print(sub_obj, " is not a folder")
            continue

        sub_final = os.path.join(final_im, folder)
        os.mkdir(sub_final)

        # Merge images based on the choice of background
        if generate_background:
            # Generate random background
            bboxes = random_bg_for_all_objects(sub_obj, sub_final, adjust_brightness, n_of_pixels)

        elif generate_background is False and background_database is None:
            print("We need a background database")
            raise RenderPipelineError("A background database is missing")
        else:
            # We draw background images from given database
            try:
                bboxes = mi.generate_for_all_objects(sub_obj,background_database ,sub_final, adjust_brightness, n_of_pixels)
            except Exception as e:
                raise RenderPipelineError("Error occured during random background generation!")

        # collate all the bboxes
        all_bbox[folder] = bboxes

    # Dump the parameters used for rendering and merging
    for folder in os.listdir(obj_poses):
        print(folder)

    # Dump all merging parameters to a json file
    all_params= {"object_set": os.path.split(obj_set)[-1],
                 "images_per_class": renders_per_class,
                 "background_generated": generate_background,
                 "background_database": os.path.split(background_database)[-1],
                 "number_of_pixels": n_of_pixels,
                 "brightness_adjusted": adjust_brightness,
                 "all_bboxes": all_bbox.__str__()
                 }
    dump_file = os.path.join(final_folder, 'mergeparams_dump.json')
    with open(dump_file, "w+") as f:
        json.dump(all_params, f, sort_keys=True, indent=4, separators=(',', ': '))

    # export everything into a zip file
    # compose the zip file name by specifying the background type
    # and a timestamp
    if generate_background:
        back_parameter = "random_bg"
    else:
        back_parameter = os.path.split(background_database)[-1]
    zip_name = os.path.join(work_dir,"final_zip",os.path.split(obj_set)[-1] + "_" + back_parameter + "_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ","_").replace(":","_"))

    make_archive(zip_name, 'zip', final_folder)
    # Clean up all generated files, apart from the zip file
    destroy_folders(work_dir, temp_folders)

    final_result = zip_name + ".zip"
    slack.send_message('Full run completed. Final zip file: ' + final_result, 'Rendering Run Completed', 'good')
    return final_result

def full_run_with_notifications(*args, **kwargs):
    """
    Exactly same as the `full_run` function but sends additional notifications
    to the Slack channel.
    Expects same parameters as `full_run`
    """
    try:
        full_run(*args, **kwargs)
    except RenderPipelineError as e:
        slack.send_message(e.value , title="RenderPipelineError occured: see terminal for details", status='danger')
        raise e
    except Exception as e:
        slack.send_message("An unknown exception occured! Please check terminal for details!",
                           title="Unknown Error occured: see console for details", status='danger')
        raise e
"""
The blender parameters. Keywords should be self explanatory.
A default parameters can be used by passing an empty dictionary
blender_attributes={}
"""

"""------------------ Running the pipeline ------------------"""
# Uncomment the below function if you want to run an example run




"""
def example_run():    

    #Function that holds all that is necessary for example run.


    blender_attributes = {
        "attribute_distribution_params": [["num_lamps","mid", 6], ["num_lamps","scale", 0.4], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
        "attribute_distribution" : []
    }

    # Set backround image database path
    sun_database = os.path.join(workspace, "bg_database","SUN_back")

    # Set object file path
    obj_set = os.path.join(workspace, "object_files","two_set_model_format")

    # Construct rendering parameters
    argument_list = []

    # An example argument dictionary using sun_database as source of background
    arguments1 = {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": 2,
        "work_dir": workspace,
        "generate_background": False,
        "background_database": sun_database,
        "blender_attributes": blender_attributes,
        "n_of_pixels": 300,
        "adjust_brightness": True
        }
    # An example argument dictionary generating random colour background
    arguments2 = {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": 2,
        "work_dir": workspace,
        "generate_background": True,
        "background_database": sun_database,
        "blender_attributes": blender_attributes,
        "n_of_pixels": 300,
        "adjust_brightness": False
        }

    # All run instructions should be appended to the `argument_list`
    argument_list.append(arguments1)
    #argument_list.append(arguments2)
    #argument_list.append(arguments3)


    # First we clean the render workspace so any leftovers from
    # failed jobs are removed
    destroy_folders(workspace, temp_folders)
    for value in argument_list:
        start_time = time.time()
        try:
            full_run(**value)
        except Exception as e:
            raise e
        print("One run done")
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__=="__main__":

    print("Running the Rendering Pipeline")
    example_run()
"""    
