"""
An object-oriented high-level wrapper for training InceptionV3 CNNs.
"""


from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.models import load_model
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras import backend as K
from time import *
import os


# For Function to feed images to model and augment images at the same time
from keras.preprocessing.image import ImageDataGenerator

# For Tensorboard & ValAccHistory
from keras.callbacks import TensorBoard, Callback

# for add_salt_pepper_noise
import numpy as np

# for leaving the program in case of invalid arguments (sys.exit(0))
import sys

# for get_config
from keras.models import Sequential

# for unzipping
import zipfile

# for customizing SGD, rmsprop
from keras.optimizers import SGD, RMSprop

# for logging
from pathlib import Path
import datetime

# for csv logging
launch_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

# Custom Image Augmentation Function
def add_salt_pepper_noise(X_img):
    # Need to produce a copy as to not modify the original image
    X_img_copy = X_img.copy()
    row, col, _ = X_img_copy.shape
    salt_vs_pepper = 0.2
    amount = 0.004
    num_salt = np.ceil(amount * X_img_copy.size * salt_vs_pepper)
    num_pepper = np.ceil(amount * X_img_copy.size * (1.0 - salt_vs_pepper))

    # Add Salt noise
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in X_img.shape]
    X_img[coords[0], coords[1], :] = 1

    # Add Pepper noise

    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in X_img.shape]
    X_img[coords[0], coords[1], :] = 0
    return X_img_copy

class ValAccHistory(Callback):
    def on_train_begin(self, logs={}):
        self.val_accs = []

    def on_epoch_end(self, epoch, logs={}):
        self.val_accs.append(logs.get('val_acc'))

class ExtraValidationCallback(Callback):
    def __init__(extra_validation):
        self.extra_validation_dir = extra_validation

    def on_train_begin(self, logs={}):
        self.val1_accs = []
        self.val1_loss = []
        self.val2_accs = []
        self.val2_loss = []
        self.train_accs = []
        self.train_loss = []
        # extra_validation_dir = self.extra_validation

    def on_epoch_end(self, epoch, logs={}):
        self.val1_accs.append(logs.get('val_acc'))
        self.val1_loss.append(logs.get('val_loss'))

        # loss, acc = self.evaluate(extra_validation_dir)
        # augmentation configuration for testing: only rescaling
        test_datagen = ImageDataGenerator(rescale=1./255)

        # generator for test data
        # similar to above but based on different augmentation function (above)
        test_generator = test_datagen.flow_from_directory(
                self.extra_validation_dir,
                target_size=(224, 224),
                batch_size=64,
                class_mode='categorical')

        loss, acc = self.model.evaluate_generator(test_generator)

        self.val2_accs.append(acc)
        self.val2_loss.append(loss)

        self.train_accs.append(logs.get('acc'))
        self.train_loss.append(logs.get('loss'))

        logging = True
        log_filename = 'log_train_double_validation.csv'

        if logging:
            print("logging now...")
            my_file = Path(log_filename)

            # write header if this is the first run
            if not my_file.is_file():
                print("writing head")
                with open(log_filename, "w") as log:
                    log.write("datetime,epoch,val1_acc,val1_loss,val2_acc,val2_loss,train_acc,train_loss\n")

            # append parameters
            with open(log_filename, "a") as log:
                log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                log.write(',')
                log.write(str(epoch))
                log.write(',')
                log.write(str(logs.get('val_acc'))),
                log.write(',')
                log.write(str(logs.get('val_loss'))),
                log.write(',')
                log.write(str(acc)),
                log.write(',')
                log.write(str(loss)),
                log.write(',')
                log.write(str(logs.get('acc'))),
                log.write(',')
                log.write(str(logs.get('loss')))
                log.write('\n')

        print('\Second Validation Set, loss: {}, acc: {}\n'.format(loss, acc))

class KerasInception:
    model = None
    input_dim = 0
    batch_size = 0
    dense_layers = 0

    def __init__(self,input_dim=150,batch_size=16,dense_layers=1,dropout=None,lr=0.0001,
                dense_dim=1024):
        self.input_dim = input_dim
        self.batch_size = batch_size
        self.dense_layers = dense_layers
        self.dropout = dropout
        self.lr = lr
        self.dense_dim = dense_dim
        self.model = None

    def assemble_model(self,train_dir):
        class_count = len(next(os.walk(train_dir))[1])

        # base pre-trained model
        base_model = InceptionV3(weights='imagenet', include_top=False)

        # global spatial average pooling layer
        x = base_model.output

        base_model.layers[-1].name = 'base_output'

        x = GlobalAveragePooling2D(name='pooling')(x)

        for i in range(self.dense_layers):
            # dropout
            if self.dropout and i == 0:
                x = Dropout(0)(x)
                print("added 0 pc dropout for layer 1")
            elif self.dropout:
                x = Dropout(self.dropout)(x)
                print("added ",self.dropout," pc dropout for layer ",i+1)

            # fully-connected layer
            x = Dense(self.dense_dim, activation='relu',name='dense'+str(i))(x)

        # logistic layer
        predictions = Dense(class_count, activation='softmax',name='softmax')(x)

        # define the model we will train
        model = Model(inputs=base_model.input, outputs=predictions)
        self.model = model

        # we want to train top layers only
        for layer in base_model.layers:
            layer.trainable = False

        # compile the model (*after* setting layers to non-trainable)
        # model.compile(optimizer=RMSprop(lr=self.lr), loss='categorical_crossentropy', metrics=['accuracy'])
        model.compile(optimizer=SGD(lr=self.lr, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    # print train classes to txt file in classes_txt_dir
    def save_class_list(self,train_dir,classes_txt_dir):
        # assemble path
        filename = "classes.txt"
        my_file = os.path.join(classes_txt_dir, filename)
        print("Writing classes.txt to:\n",my_file,'\n')
        print("Classes found:")
        for name in os.listdir(train_dir):
            if not os.path.isfile(name):
                print(name)

        # check if file already exists
        if not os.path.isfile(my_file):
            # write all folder names to txt file
            with open(my_file, "w") as classes_file:
                for name in os.listdir(train_dir):
                    # exclude files
                    if not os.path.isfile(name):
                        classes_file.write(name)
                        classes_file.write("\n")
            classes_file.close()

    # unfreeze a specified number of InceptionV3 layers
    def unfreeze(self,layers):
        inception_layers = 311
        slice = inception_layers-layers

        for layer in self.model.layers[:slice]:
           layer.trainable = False
        for layer in self.model.layers[slice:]:
           layer.trainable = True

        self.model.compile(optimizer=SGD(lr=self.lr, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

    # train a model from scratch given a set of training parameters
    # choose whether to save the model
    def train(self,train_dir,validation_dir,epochs=0,fine_tune=False, unfrozen_layers=0,
            salt_pepper=False,augmentation_params={},classes_txt_dir=None,save_model=False,
            validation_dir_2=None,steps_per_epoch=12000):
        if classes_txt_dir:
            self.save_class_list(train_dir,classes_txt_dir)

        # model can only be built here after training directory is clear
        # (for number of classes)
        # if it wasnt built before, built it now
        if not self.model:
            self.model = self.assemble_model(train_dir)

        # unfreeze specified number of Inception convolutional layer
        self.unfreeze(unfrozen_layers)

        print("Directory used for training: ",train_dir)
        print("Directory used for validation: ",validation_dir)

        # augmentation configuration for training
        if salt_pepper:
            train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    preprocessing_function=add_salt_pepper_noise,
                    **augmentation_params)
        else:
            train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    **augmentation_params)

        # generator that will read pictures found in train_dir, and
        # indefinitely generate batches of augmented image data and
        # rescales images to target_size, splits them into batches
        train_generator = train_datagen.flow_from_directory(
                train_dir,  # this is the target directory
                target_size=(self.input_dim, self.input_dim),  # all images will be resized to input_dimxinput_dim
                batch_size=self.batch_size,
                class_mode='categorical',
                shuffle=True)

        # augmentation configuration for validation: only rescaling
        validation_datagen = ImageDataGenerator(rescale=1./255)

        # generator for validation data
        # similar to above but based on different augmentation function (above)
        validation_generator = validation_datagen.flow_from_directory(
                validation_dir,
                target_size=(self.input_dim, self.input_dim),
                batch_size=self.batch_size,
                class_mode='categorical')


        # log everything in tensorboard
        tensorboard = TensorBoard(log_dir="/data/g1753002_ocado/logs/{}".format(time()),
                            histogram_freq=0,
                            batch_size=self.batch_size,
                            write_graph=True,
                            write_grads=False,
                            write_images=True,
                            embeddings_freq=0,
                            embeddings_layer_names=None,
                            embeddings_metadata=None) # histogram_freq=5

        history = ValAccHistory()

        # if a second validation_dir is provided, add an extra Keras callback
        if validation_dir_2:
            extralogger = ExtraValidationCallback(validation_dir_2)
            cbs = [tensorboard,history,extralogger]
        else:
            cbs = [tensorboard,history]

        self.model.fit_generator(
                train_generator,
                steps_per_epoch=steps_per_epoch // self.batch_size,
                epochs=epochs,
                validation_data=validation_generator,
                validation_steps=1600 // self.batch_size,
                callbacks=cbs)
                # use_multiprocessing=True,
                # workers=8)


        if fine_tune:
            self.fine_tune(train_generator,validation_generator,tensorboard)

        if save_model:
            base_path,train_folder = os.path.split(train_dir)
            full_path = os.path.join(base_path, "model.h5")
            self.save_model(full_path)

        return history

    # top 2 inception blocks layers will be trained for specified number of
    # epochs
    def fine_tune(self,train_generator,validation_generator,tensorboard,
            epochs=1):
        # we chose to train the top 2 inception blocks, i.e. we will freeze
        # the first 249 layers and unfreeze the rest:
        for layer in self.model.layers[:249]:
           layer.trainable = False
        for layer in self.model.layers[249:]:
           layer.trainable = True

        # we need to recompile the model for these modifications to take effect
        # we use SGD with a low learning rate
        self.model.compile(optimizer=SGD(lr=0.0001, momentum=0.9),
            loss='categorical_crossentropy', metrics=['accuracy'])

        # fine-tuning the top 2 inception blocks alongside the Dense layers
        self.model.fit_generator(
                train_generator,
                steps_per_epoch=2048 // self.batch_size,
                epochs=epochs,
                validation_data=validation_generator,
                validation_steps=800 // self.batch_size,
                callbacks = [tensorboard])

    # returns accuracy and loss of the trained model given a test directory
    def evaluate(self,test_dir):
        # augmentation configuration for testing: only rescaling
        test_datagen = ImageDataGenerator(rescale=1./255)

        # generator for test data
        # similar to above but based on different augmentation function (above)
        test_generator = test_datagen.flow_from_directory(
                test_dir,
                target_size=(self.input_dim, self.input_dim),
                batch_size=16,
                class_mode='categorical')

        score = self.model.evaluate_generator(test_generator)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        return score

    # expects a path to a model in h5 format (a model, not weights!)
    # model will be as when saving (i.e. compiled), can then call predict etc
    def load_model(self,file_path):
        self.model = load_model(file_path)

    # saves a model, provie a file path ending with .h5
    def save_model(self,path):
        self.model.save(path)

def get_augmentation_params(augmentation_mode):
    if augmentation_mode == 0:
        return {}
    elif augmentation_mode == 1:
        return {'rotation_range': 180}
    elif augmentation_mode == 2:
        return {'rotation_range': 180, 'zoom_range': 0.2}
    else:
        print("UNKNOWN AUGMENTATION PARAMETER! (needs to be 0, 1 or 2)")
        sys.exit(0)

def unzip_and_return_path_to_folder(path_to_zip_file):
    maindirname, filename = os.path.split(path_to_zip_file)

    new_dir = os.path.join(maindirname, filename.split('.')[0])
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(new_dir)
    zip_ref.close()

    return path_to_zip_file.split('.')[0] # name of new folder

def main():
    # train_dir = '/data/g1753002_ocado/manhattan_project/training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/train'
    train_dir = '/data/g1753002_ocado/manhattan_project/training_data/ten_set_model_official_SUN_back_2018-05-11_08_03_02/images/train'
    # validation_dir = '/data/g1753002_ocado/manhattan_project/training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/validation'
    validation_dir = '/data/g1753002_ocado/manhattan_project/training_data/ten_set_model_official_SUN_back_2018-05-11_08_03_02/images/validation'
    # test_dir = '/data/g1753002_ocado/manhattan_project/test_data/extended_test_set_ambient'
    test_dir = '/data/g1753002_ocado/manhattan_project/test_data/official_test_set_factory'

    # can add second dir if need two validation sets
    extra_validation_dir = None

    dense_layers = 1
    input_dim = 224
    batch_size = 64
    fine_tune = False # if true, some of the inceptionV3 layers will be trained for 1 epoch at the end of training
    add_salt_pepper_noise = False # if True, it adds SP noise
    augmentation_mode = 0 # 0 = no augmentation, 1 = rotation only, 2 = rotation & zoom
    epochs = 20
    # has to be a number between 0 and 311
    unfrozen_layers = 311
    learning_rate = 0.0031622777

    model = KerasInception(input_dim=input_dim,
                            batch_size=batch_size,
                            dense_layers=dense_layers)


    model.train(train_dir=train_dir,
                validation_dir=validation_dir,
                fine_tune=fine_tune,
                epochs=epochs,
                unfrozen_layers=unfrozen_layers,
                salt_pepper=add_salt_pepper_noise,
                augmentation_params=get_augmentation_params(augmentation_mode),
                validation_dir_2=extra_validation_dir)

    model.evaluate(test_dir=test_dir)

    model.save_model('occlusion_model.h5')



def main_for_pipeline_using_zip():
    logging = True
    log_filename = 'learning_rate_grid.csv'

    # get all zip files to iterate over: List parameter, Directory?


    # create grid of parameters: e.g. to a csv file, then read out line by line, once done, add 1 at the end
    learning_rate_grid = np.logspace(-6,-3,10) # originally 10 pow -5
    dropout_grid = [0,0.2,0.5]
    layer_grid = [1,2]
    batch_size_grid = [16,32,64]

    unfrozen_layers_grid = np.linspace(0,311,8)

    # input directories
    path_of_zip = '/vol/project/2017/530/g1753002/keras_test_data/train/train_test_zip2.zip'
    validation_dir = '/vol/project/2017/530/g1753002/keras_test_data/validation'
    test_dir = '/vol/project/2017/530/g1753002/keras_test_data/test'

    # load train images from one zip file
    unzipped_dir = unzip_and_return_path_to_folder(path_of_zip)
    train_dir = unzipped_dir + '/images'

    # get path for classes.txt
    main_dir, filename = os.path.split(path_of_zip)

    # go through grid of parameters
    for lr in learning_rate_grid:


        # set parameters
        input_dim = 224
        fine_tune = False # if true, some of the inceptionV3 layers will be trained for 5 epochs at the end of training
        add_salt_pepper_noise = False # if True, it adds SP noise
        augmentation_mode = 0 # 0 = no augmentation, 1 = rotation only, 2 = rotation & zoom
        epochs = 30
        unfrozen_layers = 0

        learning_rate = lr
        dense_layers = 1
        batch_size = 64
        dropout = 0

        # initialize & train model
        model = KerasInception(input_dim=input_dim,
                                batch_size=batch_size,
                                dense_layers=dense_layers,
                                dropout=dropout,
                                lr=learning_rate)


        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    fine_tune=fine_tune,
                    epochs=epochs,
                    unfrozen_layers=unfrozen_layers,
                    salt_pepper=add_salt_pepper_noise,
                    augmentation_params=get_augmentation_params(augmentation_mode),
                    classes_txt_dir=main_dir,
                    save_model=True
                    )

        # get accuracy score
        test_loss, test_acc = model.evaluate(test_dir=test_dir)

        # store accuracy & model parameters
        if logging:
            print("logging now...")
            my_file = Path(log_filename)

            # write header if this is the first run
            if not my_file.is_file():
                print("writing head")
                with open(log_filename, "w") as log:
                    log.write("datetime,epochs,learning_rate,batch_size,unfrozen_layers,input_dim,dense_layers,dropout,test_loss,test_acc\n")

            # append parameters
            with open(log_filename, "a") as log:
                log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                log.write(',')
                log.write(str(epochs))
                log.write(',')
                log.write(str(learning_rate))
                log.write(',')
                log.write(str(batch_size))
                log.write(',')
                log.write(str(unfrozen_layers))
                log.write(',')
                log.write(str(input_dim))
                log.write(',')
                log.write(str(dense_layers))
                log.write(',')
                log.write(str(dropout))
                log.write(',')
                log.write(str(test_loss))
                log.write(',')
                log.write(str(test_acc))
                log.write('\n')


# main()

# main_for_pipeline()

grid_search()
