from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from time import *

# load model
from keras.models import load_model

# For Function to feed images to model and augment images at the same time
from keras.preprocessing.image import ImageDataGenerator

# For Tensorboard
from keras.callbacks import TensorBoard


test_dir = '/vol/project/2017/530/g1753002/keras_test_data/test'

model = load_model('my_model.h5')

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=16,
        class_mode='categorical')

print("calculating ...")

score = model.evaluate_generator(test_generator)

print('Test loss:', score[0])
print('Test accuracy:', score[1])


# generator for predictions, if needed

# pred_datagen = ImageDataGenerator()
#
# pred_generator = pred_datagen.flow_from_directory(
#         test_dir,
#         target_size=(150, 150),
#         batch_size=16,
#         class_mode=None,  # only data, no labels
#         shuffle=False)  # keep data in same order as labels
