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

model = load_model('my_model.h5')

preds = model.predict(test_datagen, batch_size=16)
tf_session = K.get_session()

print(preds)
