from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras import optimizers
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

batch_size = 16
class_count = len(next(os.walk('/vol/project/2017/530/g1753002/keras_test_data/train'))[1])
train_data_dir = '/homes/mzw17/Downloads/train'
validation_data_dir = '/homes/mzw17/Downloads/train'
test_dir = '/vol/project/2017/530/g1753002/experiment1'

# augmentation configuration for training
# need to add salt&pepper noise, rotation, light
# no horizontal flips for most classes
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

# augmentation configuration for testing: only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of train_data_dir, and indefinitely generate
# batches of augmented image data
# it also rescales images to 150x150 and splits them into batches
# (instead of loading all images directly into GPU memory)
train_generator = train_datagen.flow_from_directory(
        train_data_dir,  # this is the target directory
        target_size=(224, 224),  # all images will be resized to 150x150
        batch_size=16,
        class_mode='categorical')

# generator for validation data
# similar to above but based on different augmentation function (above)
validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(150, 150),
        batch_size=16,
        class_mode='categorical')

# generator for test data
# similar to above but based on different augmentation function (above)
test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(224, 224),
        batch_size=16,
        class_mode='categorical')

# base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# fully-connected layer
x = Dense(1024, activation='relu')(x)
# logistic layer
predictions = Dense(class_count, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# we want to train top layers only
for layer in base_model.layers:
    layer.trainable = False


adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, amsgrad=False)
# compile the model (*after* setting layers to non-trainable)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

# log everything in tensorboard
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# train the model on the new data for a few epochs
model.fit_generator(
        train_generator,
        steps_per_epoch=2000 // batch_size,
        epochs=5,
        validation_data=validation_generator,
        validation_steps=800 // batch_size,
        callbacks = [tensorboard])

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(
        train_generator,
        steps_per_epoch=2000 // batch_size,
        epochs=5,
        validation_data=validation_generator,
        validation_steps=800 // batch_size)


model.save_weights('first_try.h5')  # always save your weights after training or during training
model.save('experimental_model_1.h5')

score = model.evaluate_generator(test_generator)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# How to do predictions: https://datascience.stackexchange.com/questions/13894/how-to-get-predictions-with-predict-generator-on-streaming-test-data-in-keras

# # predictions
# print("==== Predictions ====")
# # since we dont have the test data loaded yet, we use a generator (again) to load it in one by one and make a prediction for each
# # see https://keras.io/models/sequential/#sequential-model-methods
# # we cannot use the standard predict function, which only takes in one data point and makes a prediction for it
# pred_datagen = ImageDataGenerator()
#
# pred_generator = pred_datagen.flow_from_directory(
#         test_dir,
#         target_size=(150, 150),
#         batch_size=16,
#         class_mode=None,  # only data, no labels
#         shuffle=False)  # keep data in same order as labels
#
# probabilities = model.predict_generator(pred_generator, 2000)
#
# print("==== Test Accuracy ====")
# print(probabilities)
#
# # calculate accuracy







# THIS CODE COULD BE ADDED BEFORE SAVING FOR SLIGHT IMPROVEMENT IN PERFORMANCE
# # at this point, the top layers are well trained and we can start fine-tuning
# # convolutional layers from inception V3. We will freeze the bottom N layers
# # and train the remaining top layers.
#
