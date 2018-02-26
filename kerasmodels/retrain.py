from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from time import *
import os

# many parts come from here: https://keras.io/applications/ see Fine-tune InceptionV3 on a new set of classes
# some code from here: https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

# here's a model which uses bottleneck caching: https://gist.github.com/Thimira/354b90d59faf8b0d758f74eae3a511e2
# our current model doesnt cache, instead it generates a new distorted image every time

# For Function to feed images to model and augment images at the same time
from keras.preprocessing.image import ImageDataGenerator

# For Tensorboard
from keras.callbacks import TensorBoard


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
                rescale=1./255)
                # shear_range=0.2,
                # zoom_range=0.2,
                # horizontal_flip=True)


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



# THIS CODE COULD BE ADDED BEFORE SAVING FOR SLIGHT IMPROVEMENT IN PERFORMANCE
# # at this point, the top layers are well trained and we can start fine-tuning
# # convolutional layers from inception V3. We will freeze the bottom N layers
# # and train the remaining top layers.
#
# # let's visualize layer names and layer indices to see how many layers
# # we should freeze:
# for i, layer in enumerate(base_model.layers):
#    print(i, layer.name)
#
# # we chose to train the top 2 inception blocks, i.e. we will freeze
# # the first 249 layers and unfreeze the rest:
# for layer in model.layers[:249]:
#    layer.trainable = False
# for layer in model.layers[249:]:
#    layer.trainable = True
#
# # we need to recompile the model for these modifications to take effect
# # we use SGD with a low learning rate
# from keras.optimizers import SGD
# model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
#
# # we train our model again (this time fine-tuning the top 2 inception blocks
# # alongside the top Dense layers
# model.fit_generator(
#         train_generator,
#         steps_per_epoch=2000 // batch_size,
#         epochs=50,
#         validation_data=validation_generator,
#         validation_steps=800 // batch_size)
