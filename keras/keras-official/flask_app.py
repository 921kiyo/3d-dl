# from keras.applications.inception_v3 import InceptionV3
# from keras.preprocessing import image
# from keras.models import Model
# from keras.layers import Dense, GlobalAveragePooling2D
# from keras import backend as K
# from keras import optimizers
# from time import *
# import os
from keras.models import load_model

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
# import argparse

from flask import Flask, request

# initialize the input image shape (224x224 pixels) along with
# the pre-processing function (this might need to be changed
# based on which model we use to classify our image)
inputShape = (224, 224)
preprocess = preprocess_input

model = load_model('production_model_1.h5')


UPLOAD_FOLDER = '/home/mforcexvi1/mysite'

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/image')
def root():
    return app.send_static_file('image.jpg')

@app.route('/hello')
def predict1():
    return '<!DOCTYPE html> <html> <body> <form action="/predict" method="POST" enctype="multipart/form-data"> <input type="file" name="my_image" accept="image/*"> <input type="submit"> </form> </body> </html>'

@app.route('/predict', methods=['POST'])
def predict():
    # load the input image using the Keras helper utility while ensuring
    # the image is resized to `inputShape`, the required input dimensions
    # for the ImageNet pre-trained network
    print("[INFO] loading and pre-processing image...")
    if request.method == 'POST':
      f = request.files['my_image']
      f.save('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg')

    # file = request.files['my_image']
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
    image = load_img('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg', target_size=inputShape)
    image = img_to_array(image)

    # our input image is now represented as a NumPy array of shape
    # (inputShape[0], inputShape[1], 3) however we need to expand the
    # dimension by making the shape (1, inputShape[0], inputShape[1], 3)
    # so we can pass it through thenetwork
    image = np.expand_dims(image, axis=0)

    # pre-process the image using the appropriate function based on the
    # model that has been loaded (i.e., mean subtraction, scaling, etc.)
    image = preprocess(image)

    # classify the image
    print("[INFO] classifying image")
    preds = model.predict(image)
    print(preds)
    cheese_value = '{:.3f}'.format(preds[0][0]*100)
    yogurt_value = '{:.3f}'.format(preds[0][1]*100)

    print("Cheese: " + cheese_value + "%")
    print("Yogurt: " + yogurt_value + "%")
    #return "Cheese: " + cheese_value + "% and " + "Yogurt: " + yogurt_value + "%"
    return '<!DOCTYPE html> <html> <body> Cheese: ' + cheese_value + '% <br> Yogurt: ' + yogurt_value + '% <br> <img src="image" width="500" height="500"> </body> </html>'

@app.route('/123')
def predict2():
    # file = request.files['my_image']
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
    #image = load_img('/home/mforcexvi1/Lobster/keras/keras-official/image.jpg', target_size=inputShape)
    image = load_img('/homes/mzw17/Lobster/keras/keras-official/image.jpg', target_size=inputShape)
    image = img_to_array(image)

    # our input image is now represented as a NumPy array of shape
    # (inputShape[0], inputShape[1], 3) however we need to expand the
    # dimension by making the shape (1, inputShape[0], inputShape[1], 3)
    # so we can pass it through thenetwork
    image = np.expand_dims(image, axis=0)

    # pre-process the image using the appropriate function based on the
    # model that has been loaded (i.e., mean subtraction, scaling, etc.)
    image = preprocess(image)

    # classify the image
    print("[INFO] classifying image")
    preds = model.predict(image)
    print(preds)
    cheese_value = '{:.3f}'.format(preds[0][0]*100)
    yogurt_value = '{:.3f}'.format(preds[0][1]*100)

    print("Cheese: " + cheese_value + "%")
    print("Yogurt: " + yogurt_value + "%")
    return "Cheese: " + cheese_value + "% and " + "Yogurt: " + yogurt_value + "%"
