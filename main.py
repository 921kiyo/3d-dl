"""
main file to choose render and neural network parameters
input:
    obj files stored in render_workspace/object_files
    backgrounds stored in render_workspace/bg_database
    path to blender executable
    directories of validation data and test data
output: trained model as h5 file
"""

from kerasmodels import retrain
from src.rendering import render_pipeline
import os

"This script generates artefacts which are saved in folder /artefacts"

def main():
    ############################################################################
    ################################ PARAMETERS ################################
    ############################################################################

    ############################### INPUT PATHS ###############################

    # test and validation data
    validation_dir = os.path.join(os.getcwd(),'demo_images','test')
    test_dir = os.path.join(os.getcwd(),'demo_images','validation')

    # path to blender executable
    # bl_path = 'PATH/TO/BLENDER/INSTALLATION'
    bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender'

    # path to render workspace folder
    workspace = os.path.join(os.getcwd(),"render_workspace") # relative path to provided workspace

    # path to folder containing a set of .model files
    obj_set = os.path.join(workspace, 'object_files','two_set') # obj files

    model_filename = "model.h5"

    ############################################################################


    ############################## NEURAL NETWORK ##############################

    # Neural Network Parameters
    dense_layers = 1
    dense_dim = 1024
    dropout = 0
    fine_tune = False # if true, some of the inceptionV3 layers will be trained for 5 epochs at the end of training
    add_salt_pepper_noise = False # if True, it adds SP noise
    augmentation_mode = 0 # 0 = no augmentation, 1 = rotation only, 2 = rotation & zoom
    epochs = 10
    input_dim = 224

    ############################################################################

    ################################ BACKGROUND ################################

    # Choose background type: 'SUN', 'random', 'white', 'indoor', 'outdoor'
    background_type = 'indoor'

    # Choose whether to adjust background brightness to product brightness
    adjust_brightness = False

    ############################################################################

    ################################ RENDERING ################################

    # choose how many images to render per class
    renders_per_class = 10

    # Rendering Parameters
    blender_attributes = {
        "attribute_distribution_params":
            [
                # number of lamps is a DISCRETE UNIFORM DISTRIBUTION over NON_NEGATIVE INTEGERS,
                # params l and r are lower and upper bounds of distributions, need to be positive integers
                ["num_lamps","mid", 6], ["num_lamps","scale", 0.3],

                # lamp energy is a TRUNCATED NORMAL DISTRIBUTION, param descriptions same as above
                ["lamp_energy", "mu", 5000.0], ["lamp_energy", "sigmu", 0.3],

                # camera location is a COMPOSITE SHELL RING DISTRIBUTION
                # param normals define which rings to use, based on their normals, permitted values are 'X','Y','Z' and a combination of the three
                # phi sigma needs to be non-negative, and defines the spread of the ring in terms of degrees
                # phi sigma of roughly 30.0 corresponds to a unifrom sphere
                ["camera_loc","phi_sigma", 10.0],

                # camera radius is a Truncated Normal Distribution
                ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.3],
            ],
        "attribute_distribution" : []
    }

    ############################################################################

    ############################################################################
    ################################ EXECUTION ################################
    ############################################################################

    # Set backround image database path
    background_database = os.path.join(workspace, "bg_database",background_type)

    # determine whether to generate random backgrounds
    generate_background = False
    if background_type is 'random':
        generate_background = True

    # construct rendering parameters
    arguments = {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": renders_per_class,
        "work_dir": workspace,
        "generate_background": generate_background,
        "background_database": background_database,
        "blender_attributes": blender_attributes
        }

    # run blender pipeline and produce a zip with all rendered images
    path_of_zip = render_pipeline.full_run(**arguments)

    # load train images from the zip file
    unzipped_dir = retrain.unzip_and_return_path_to_folder(path_of_zip)
    train_dir = unzipped_dir + '/images'

    # get path for classes.txt
    main_dir, filename = os.path.split(path_of_zip)

    # default batch size = 64 but choose lower batch size if few images rendered
    batch_size = min(renders_per_class//2,64)

    # initialize & train model
    model = retrain.KerasInception(input_dim=input_dim,
                            batch_size=batch_size,
                            dense_layers=dense_layers,
                            dropout=dropout,
                            dense_dim=dense_dim)

    # train the network
    history = model.train(train_dir=train_dir,
                validation_dir=validation_dir,
                fine_tune=fine_tune,
                epochs=epochs,
                salt_pepper=add_salt_pepper_noise,
                augmentation_params=retrain.get_augmentation_params(augmentation_mode),
                classes_txt_dir=main_dir,
                save_model=True,
                steps_per_epoch=renders_per_class
                )

    loss, acc = model.evaluate(test_dir)

    print("test accuracy of the model is: ", acc)

    print("Model is being saved in ",os.path.join(os.getcwd(),model_filename))
    model.save_model(os.path.join(os.getcwd(),model_filename))

    if os.path.exists(path_of_zip):
        os.remove(path_of_zip)

if __name__== "__main__":
  main()
