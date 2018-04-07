# Hacky way to import render_pipeline
# import sys
# sys.path.append('src/rendering/')
# sys.path.insert(0, '~/ocado/Lobster/src/rendering/')
from rendering import render_pipeline
# import render_pipeline
import retrain

# for logging
from pathlib import Path
import datetime

# for BO
from bayes_opt import BayesianOptimization

import pickle

# SLACK
from slackclient import SlackClient
sc = SlackClient("xoxp-273685211557-273369142960-343515639718-246d19b1bb30d4a9c436d25dced63476",)

# input directories
path_of_zip = '' # TODO does the imported retrain function take this path?
validation_dir = '/vol/project/2017/530/g1753002/manhattan_project/validation_data/official_validation_set_ambient'
test_dir = '/vol/project/2017/530/g1753002/manhattan_project/test_data/official_test_set_ambient'


def evaluate_pipeline(learning_rate,dense_layers,batch_size,dropout,
        num_lamps_mid, num_lamps_scale, lamp_energy_mu, lamp_energy_sigmu,
        camera_loc_phi_sigma, camera_radius_mu,camera_radius_sigmu):

    background_type = 'white'
    adjust_brightness = False


    bl_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
    obj_set = os.path.join(workspace, 'object_files','ten_set_model_format') # obj files

    # turn float inputs from BO to ints
    dense_layers = int(dense_layers + 0.5)
    batch_size = int(batch_size + 0.5)*16
    num_lamps_mid = int(num_lamps_mid + 0.5)

    logging = True
    log_filename = 'log_bo_06_04_2018.csv'

    # params = {}
    # # neural net
    # params['learning_rate'] = learning_rate
    # params['dense_layers'] = dense_layers
    # params['batch_size'] = batch_size
    # params['dropout'] = dropout
    #
    # # blender
    # params['num_lamps_mid'] = num_lamps_mid
    # params['num_lamps_scale'] = num_lamps_scale
    # params['lamp_energy_mu'] = lamp_energy_mu
    # params['lamp_energy_sigmu'] = lamp_energy_sigmu
    # params['camera_loc_phi_sigma'] = camera_loc_phi_sigma
    # params['camera_loc_normals'] = camera_loc_normals
    # params['camera_radius_mu'] = camera_radius_mu
    # params['camera_radius_sigmu'] = camera_radius_sigmu
    #
    # # background
    # # `indoor`, `outdoor`, `SUN_back`, `white`
    # params['background_type'] = background_type
    # params['adjust_brightness'] = adjust_brightness

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

                #camera radius is a Truncated Normal Distribution
                ["camera_radius", "mu", 6.0], ["camera_radius", "sigmu", 0.3],
            ],
        "attribute_distribution" : []
    }

    # Set backround image database path
    background_database = os.path.join(workspace, "bg_database",background_type)


    # Construct rendering parameters
    argument_list = []

    arguments = {
        "obj_set": obj_set,
        "blender_path": bl_path,
        "renders_per_class": 2,
        "work_dir": workspace,
        "generate_background": False,
        "background_database": background_database,
        "blender_attributes": blender_attributes
        }


    path_of_zip = render_pipeline.full_run(**arguments)

    best_validation_accuracy = retrain.train_model_external(learning_rate,dense_layers,batch_size,dropout)

    text = "Accuracy in this run:"+str(best_validation_accuracy)
    sc.api_call("chat.postMessage",channel="CA26521FW",
        text=text,username="Botty",
        unfurl_links="true")


    # Logging everything in a CSV just in case
    if logging:
        print("logging now...")
        my_file = Path(log_filename)

        # write header if this is the first run
        if not my_file.is_file():
            print("writing head")
            with open(log_filename, "w") as log:
                log.write("learning_rate,dense_layers,batch_size,dropout,\
                num_lamps_mid,num_lamps_scale,lamp_energy_mu,lamp_energy_sigmu,\
                camera_loc_phi_sigma,camera_radius_mu,camera_radius_sigmu,\
                background_type,adjust_brightness, \
                best_validation_accuracy\n")

        # append parameters
        with open(log_filename, "a") as log:
            log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            log.write(',')
            # Neural Network
            log.write(str(learning_rate))
            log.write(',')
            log.write(str(dense_layers))
            log.write(',')
            log.write(str(batch_size))
            log.write(',')
            log.write(str(dropout))
            log.write(',')
            # Blender
            log.write(str(num_lamps_mid))
            log.write(',')
            log.write(str(num_lamps_scale))
            log.write(',')
            log.write(str(lamp_energy_mu))
            log.write(',')
            log.write(str(lamp_energy_sigmu))
            log.write(',')
            log.write(str(camera_loc_phi_sigma))
            log.write(',')
            log.write(str(camera_radius_mu))
            log.write(',')
            log.write(str(camera_radius_sigmu))
            log.write(',')
            # Background
            log.write(background_type)
            log.write(',')
            log.write(str(adjust_brightness))
            log.write(',')
            # Result
            log.write(str(best_validation_accuracy))
            log.write(',')
            log.write('\n')

    return best_validation_accuracy

def continue_bayes_optimization(bo_instance_filename,iterations,kappa):
    # TODO: Function that takes pickled BO and can explore based on it
    pickle.load(open(bo_instance_filename,"rb"))
    nnBO.maximize(n_iter=iterations, kappa=kappa)
    return

def bayes_optimization(iterations):
    gp_params = {"alpha": 1e-5}

    nnBO = BayesianOptimization(train_model,
        {'learning_rate': (1e-07, 1e-03),
        'batch_size': (0.5001, 4.4999),
        'dropout': (0, 0.5),
        'dense_layers': (0.5001, 3.4999),
        'num_lamps_mid': (1,20),
        'num_lamps_scale': (0,1),
        'lamp_energy_mu': (0,30000),
        'lamp_energy_sigmu': (0,3),
        'camera_loc_phi_sigma': (0,30),
        'camera_radius_mu': (2,12),
        'camera_radius_sigmu': (0,3)
        }
        )
    nnBO.explore({'learning_rate': [1.1787686347935867e-05],
            'dropout': [0.0],
            'dense_layers': [2.0],
            'batch_size': [4.5]
            })

    """Initial Queries"""
    # loop to try a second time in case of error
    errcount = 0
    for i in range(2):
        try:
            nnBO.maximize(init_points=5, n_iter=1, kappa=5) # would be just this line without errorhandling
        except KeyBoardInterrupt:
            raise
        except:
            if errcount == 1:
                text = "Exception occured twice in initialization, aborting!"
                print(text)
                sc.api_call("chat.postMessage",channel="CA26521FW",
                    text=text,username="Botty",
                    unfurl_links="true")
                raise
            errcount =+ 1


    """Query Loop (save after every iteration)"""
    for i in range(iterations):
        # loop to try a second time in case of error
        errcount = 0
        for i in range(2):
            try:
                nnBO.maximize(n_iter=1, kappa=4) # would be just this line without errorhandling
            except KeyBoardInterrupt:
                raise
            except:
                if errcount == 1:
                    text = "Exception occured twice in optimization, aborting!"
                    print(text)
                    sc.api_call("chat.postMessage",channel="CA26521FW",
                        text=text,username="Botty",
                        unfurl_links="true")
                    raise
                errcount =+ 1

        # save after every iteration
        filename = 'bo_instance' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + '.p'
        pickle.dump(nnBO,open(filename,'wb'))

        # print current overall best_validation_accuracy
        print(nnBO.res['max'])
