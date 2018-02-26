from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from time import *
import os


# For Function to feed images to model and augment images at the same time
from keras.preprocessing.image import ImageDataGenerator

# For Tensorboard
from keras.callbacks import TensorBoard

# for add_salt_pepper_noise
import numpy as np

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


class KerasInception:
    model = None
    input_dim = 0
    batch_size = 0

    def __init__(self,input_dim=150,batch_size=16):
        self.input_dim = input_dim
        self.batch_size = batch_size

    def assemble_model(self,train_dir):
        class_count = len(next(os.walk(train_dir))[1])

        # base pre-trained model
        base_model = InceptionV3(weights='imagenet', include_top=False)

        # global spatial average pooling layer
        x = base_model.output

        base_model.layers[-1].name = 'base_output'

        x = GlobalAveragePooling2D(name='pooling')(x)
        # fully-connected layer
        x = Dense(1024, activation='relu',name='dense')(x)
        # logistic layer
        predictions = Dense(class_count, activation='softmax',name='softmax')(x)

        # this is the model we will train
        model = Model(inputs=base_model.input, outputs=predictions)

        # we want to train top layers only
        for layer in base_model.layers:
            layer.trainable = False

        # compile the model (*after* setting layers to non-trainable)
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    def train(self,train_dir,validation_dir,epochs=5):
        # model can only be built here after training directory is clear
        # (for number of classes)
        self.model = self.assemble_model(train_dir)

        print("Directory used for training: ",train_dir)
        print("Directory used for validation: ",validation_dir)
        # augmentation configuration for training
        # need to add salt&pepper noise, rotation, light
        # no horizontal flips for most classes
        train_datagen = ImageDataGenerator(
                rescale=1./255,
                zoom_range=0.2,
                preprocessing_function=add_salt_pepper_noise,
                # rotation_range=180,
                horizontal_flip=False)


        # this is a generator that will read pictures found in
        # subfolers of train_dir, and indefinitely generate
        # batches of augmented image data and
        # rescales images to the specified target_size and splits them into batches
        # (instead of loading all images directly into GPU memory)
        train_generator = train_datagen.flow_from_directory(
                train_dir,  # this is the target directory
                target_size=(self.input_dim, self.input_dim),  # all images will be resized to input_dimxinput_dim
                batch_size=self.batch_size,
                class_mode='categorical')

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
        tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

        # train the model on the new data for a few epochs
        self.model.fit_generator(
                train_generator,
                steps_per_epoch=2000 // self.batch_size,
                epochs=epochs,
                validation_data=validation_generator,
                validation_steps=800 // self.batch_size,
                callbacks = [tensorboard])

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

    def save_model(self,name):
        self.model.save(name)


def main():
    train_dir = '/vol/project/2017/530/g1753002/keras_test_data/train'
    validation_dir = '/vol/project/2017/530/g1753002/keras_test_data/validation'
    test_dir = '/vol/project/2017/530/g1753002/keras_test_data/test'

    model = KerasInception(input_dim=150,batch_size=16)
    model.train(train_dir=train_dir,validation_dir=validation_dir)
    model.evaluate(test_dir=test_dir)

main()
