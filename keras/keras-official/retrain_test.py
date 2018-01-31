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


# model = define_top_model()
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# load model and make prediction then
# model_weights_file = 'first_try.h5'
#
# model.load_weights(model_weights_file)

test_dir = '/homes/sk5317/ocado/Swen/test'

model = load_model('my_model.h5')

pred_datagen = ImageDataGenerator()

pred_generator = pred_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=16,
        class_mode=None,  # only data, no labels
        shuffle=False)  # keep data in same order as labels

# preds = model.predict(pred_generator, batch_size=16)
preds = model.predict_generator(pred_generator, 2000)

tf_session = K.get_session()

print(preds)
