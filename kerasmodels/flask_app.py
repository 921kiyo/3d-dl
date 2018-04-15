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

from flask import Flask, request, jsonify

import hashlib
import time
import operator

from PIL import Image

# initialize the input image shape (224x224 pixels) along with
# the pre-processing function (this might need to be changed
# based on which model we use to classify our image)
inputShape = (224, 224)
preprocess = preprocess_input

#model = load_model('production_model_1.h5')
#model = load_model('/vol/project/2017/530/g1753002/Trained_Models/8_class_model.h5')
model = load_model('/data/11th_apr.h5')

UPLOAD_FOLDER = '/vol/project/2017/530/g1753002/Flask_App/'

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/image')
def root1():
    return app.send_static_file('image.jpg')

@app.route('/<image_file>')
def root(image_file):
    return app.send_static_file('image_file' + '.jpg')

# Welcome page
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
      my_hash = hashlib.sha1()
      my_hash.update(str(time.time()).encode('utf-8'))
      short_hash = my_hash.hexdigest()[:10]
      filepath = '/vol/project/2017/530/g1753002/Flask_App/' + short_hash + '.jpg'
      #f.save('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg')
      f.save(filepath)

    # file = request.files['my_image']
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
    #image = load_img('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg', target_size=inputShape)
    image = load_img(filepath, target_size=inputShape)
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
    anchor_value = '{:.3f}'.format(preds[0][0]*100)
    cheese_value = '{:.3f}'.format(preds[0][1]*100)
    clinique_value = '{:.3f}'.format(preds[0][2]*100)
    coconutwater_value = '{:.3f}'.format(preds[0][3]*100)
    neutrogena_value = '{:.3f}'.format(preds[0][4]*100)
    nivea_value = '{:.3f}'.format(preds[0][5]*100)
    utterlybutterly_value = '{:.3f}'.format(preds[0][6]*100)
    yogurt_value = '{:.3f}'.format(preds[0][7]*100)

    print("Anchor: " + anchor_value + "%")
    print("Cheese: " + cheese_value + "%")
    print("Clinique: " + clinique_value + "%")
    print("Coconut Water: " + coconutwater_value + "%")
    print("Neutrogena: " + neutrogena_value + "%")
    print("Nivea: " + nivea_value + "%")
    print("Utterly Butterly: " + utterlybutterly_value + "%")
    print("Yogurt: " + yogurt_value + "%")
    #return "Cheese: " + cheese_value + "% and " + "Yogurt: " + yogurt_value + "%"
    return '<!DOCTYPE html> <html> <body> Anchor: ' + anchor_value + '% <br> Cheese: ' + cheese_value + '% <br> Clinique: ' + clinique_value + '% <br> Coconut Water: ' + coconutwater_value + '% <br> Neutrogena: ' + neutrogena_value + '% <br> Nivea: ' + nivea_value + '% <br> UtterlyButterly: ' + utterlybutterly_value + '% <br>Yogurt: ' + yogurt_value + '% <br> <img src="'+ short_hash + '" width="500" height="500"> </body> </html>'


@app.route('/api', methods=['POST'])
def predict_api():
    # load the input image using the Keras helper utility while ensuring
    # the image is resized to `inputShape`, the required input dimensions
    # for the ImageNet pre-trained network
    print("[INFO] loading and pre-processing image...")
    if request.method == 'POST':
      f = request.files['my_image']
      my_hash = hashlib.sha1()
      my_hash.update(str(time.time()).encode('utf-8'))
      short_hash = my_hash.hexdigest()[:10]
      #filepath = '/vol/project/2017/530/g1753002/Flask_App/' + short_hash + '.jpg'
      filepath = '/data/Flask_App/' + short_hash + '.jpg'
      #f.save('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg')
      f.save(filepath)

    # file = request.files['my_image']
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
    #image = load_img('/homes/mzw17/Lobster/keras/keras-official/static/image.jpg', target_size=inputShape)

    #Process image in PIL (crop to square)
    # img = Image.open(filepath)
    # width, height = img.size
    # print(width, height)
    # crop_amount = width - height
    # area = (crop_amount, 0, width, height)
    # cropped_img = img.crop(area)
    # print(cropped_img.size)
    # cropped_img.save('/data/reference_img.jpg')

    image = load_img(filepath, target_size=inputShape)
    # image = load_img('/data/reference_img.jpg', target_size=inputShape)
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
    # anchor_value = '{:.3f}'.format(preds[0][0]*100)
    # cheese_value = '{:.3f}'.format(preds[0][1]*100)
    # clinique_value = '{:.3f}'.format(preds[0][2]*100)
    # coconutwater_value = '{:.3f}'.format(preds[0][3]*100)
    # neutrogena_value = '{:.3f}'.format(preds[0][4]*100)
    # nivea_value = '{:.3f}'.format(preds[0][5]*100)
    # utterlybutterly_value = '{:.3f}'.format(preds[0][6]*100)
    # yogurt_value = '{:.3f}'.format(preds[0][7]*100)
    anchor_value = '{:.3f}'.format(preds[0][0]*100)
    coconutwater_value = '{:.3f}'.format(preds[0][1]*100)
    cottagecheese_value = '{:.3f}'.format(preds[0][2]*100)
    halloumi_value = '{:.3f}'.format(preds[0][3]*100)
    liberte_value = '{:.3f}'.format(preds[0][4]*100)
    mangoyogurt_value = '{:.3f}'.format(preds[0][5]*100)
    soup_value = '{:.3f}'.format(preds[0][6]*100)
    soymilk_value = '{:.3f}'.format(preds[0][7]*100)
    squashums_value = '{:.3f}'.format(preds[0][8]*100)
    strawberryyogurt_value = '{:.3f}'.format(preds[0][9]*100)

    print("Anchor: " + anchor_value + "%")
    print("Coconut Water: " + coconutwater_value + "%")
    print("Cottage Cheese: " + cottagecheese_value + "%")
    print("Halloumi: " + halloumi_value + "%")
    print("Liberte: " + liberte_value + "%")
    print("Mango Yogurt: " + mangoyogurt_value + "%")
    print("Soup: " + soup_value + "%")
    print("Soymilk: " + soymilk_value + "%")
    print("Squashsums: " + squashums_value + "%")
    print("Strawberry Yogurt: " + strawberryyogurt_value + "%")

    classified = {"Anchor": float(anchor_value), "Coconut Water": float(coconutwater_value), "Cottage Cheese": float(cottagecheese_value), "Halloumi": float(halloumi_value), "Liberte": float(liberte_value), "Mango Yogurt": float(mangoyogurt_value), "Soup": float(soup_value), "Soymilk": float(soymilk_value), "Squashums": float(squashums_value), "Strawberry Yg.": float(strawberryyogurt_value)}

    max_key = max(classified.items(), key=operator.itemgetter(1))[0]

    max_value = classified.get(max_key, "Error")

    result = {"max_class": max_key, "max_value": str(max_value)}

    return jsonify(result)
    #return "Cheese: " + cheese_value + "% and " + "Yogurt: " + yogurt_value + "%"
    # '<!DOCTYPE html> <html> <body> Anchor: ' + anchor_value + '% <br> Cheese: ' + cheese_value + '% <br> Clinique: ' + clinique_value + '% <br> Coconut Water: ' + coconutwater_value + '% <br> Neutrogena: ' + neutrogena_value + '% <br> Nivea: ' + nivea_value + '% <br> UtterlyButterly: ' + utterlybutterly_value + '% <br>Yogurt: ' + yogurt_value + '% <br> <img src="'+ short_hash + '" width="500" height="500"> </body> </html>'



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
