import os
import math # for floor
import glob # for listing all files in a dir
import random # to pick a random file
import shutil # to move files

path = "D:\\PycharmProjects\\Lobster\\data\\logs\\rendering_debug_logs\\test_run_bbox\\ten_set_model_format_SUN_back_2018-05-05_00_21_25\\images"
validation_percentage = 0.2

# counts files in all subfolders
def file_count(path):
  count = 0
  for f in os.listdir(path):
    child = os.path.join(path, f)
    if os.path.isdir(child):
      child_count = file_count(child)
      count += child_count
    else:
      count += 1
  return count

# splitting % of files from path/train, moves them to validation subfolder
# creates validation subfolder if it doesnt exist
def split_train_to_validation(path,percentage_split):
    # create the two paths, assuming they are ending with validation and train
    validation_path = os.path.join(path, 'validation')
    train_path = os.path.join(path, 'train')

    # if the validation folder doesnt exist yet, create it
    if not os.path.exists(validation_path):
        os.makedirs(validation_path)

    # check if validation folder already has files, if it does, assert
    # that it is intentional
    if file_count(validation_path) > 0:
        text = input("there are already images in the validation set, confirm with 'Y': ")
        if text is not "Y":
            print("Aborting splitting")
            return
    print("Splitting now ...")

    # get all class subfolders
    child_directories = next(os.walk(train_path))[1]

    val_filenames = []

    for child in child_directories:

        print("splitting images in folder",child,"...")
        # concat child directories for each class
        child_train_path = os.path.join(train_path, child)
        child_validation_path = os.path.join(validation_path, child)

        # if the folder for this class doenst exist in validation, create it
        if not os.path.exists(child_validation_path):
            os.makedirs(child_validation_path)

        # determine number of images we want to move from train to validation
        train_count = file_count(child_train_path)
        validation_count = math.floor(train_count * percentage_split)

        # get list of all file paths
        file_path = os.path.join(child_train_path, '*.*')
        train_list = glob.glob(file_path)

        # for validation_count, we pick a random file in directory
        for i in range(validation_count):
            # pick a random image from the folder, remove the image from list
            image_path = random.choice(train_list)
            train_list.remove(image_path)

            # get the name of the image
            image_name = os.path.basename(image_path)

            # concat path to name to get new dir
            new_path = os.path.join(child_validation_path, image_name)
            val_filenames.append(new_path)

            # verbose
            # print("moving:", image_path)
            # print("to:", new_path)

            # perform the move
            shutil.move(image_path, new_path)

    print("Done splitting!")
    return val_filenames

# call the function
if __name__ == "main":
    split_train_to_validation(path,validation_percentage)

