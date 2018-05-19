from flask import jsonify

import hashlib
import time
import operator

import os.path

from PIL import Image

import numpy as np

from keras.models import load_model

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img


"""
Function to generate a unique filepath based on a hash of the current time

Inputs:
String containing path to Folder where filepath should be generated

Return value:
String containing unique filepath
"""
def generate_unique_filepath(path_to_folder):
    my_hash = hashlib.sha1()
    my_hash.update(str(time.time()).encode('utf-8'))
    short_hash = my_hash.hexdigest()[:10]

    filepath = path_to_folder + short_hash + '.jpg'

    return filepath


"""
Crops image from rectangular to square, saves cropped image in original location

Inputs:
Filepath: Path to image to be cropped
"""
def crop_image(filepath):
    img = Image.open(filepath)
    width, height = img.size
    print(width, height)

    area = (0, 0, width, width)
    cropped_img = img.crop(area)
    print(cropped_img.size)
    cropped_img.save(filepath)


"""
Runs target image through Neural Network to get predicted results

Inputs:
Filepath: Path to image to be classified
Model: Neural Network Model (Keras)

Return value:
Predictions: Array of predictions from Neural Network
"""
def get_predictions(filepath, model):

    inputShape = (224, 224)
    preprocess = preprocess_input

    image = load_img(filepath, target_size=inputShape)
    image = img_to_array(image)

    image = np.expand_dims(image, axis=0)

    # pre-process the image
    image /= 255.

    # classify the image
    print("[INFO] classifying image")
    preds = model.predict(image)
    print(preds)

    return preds


"""
Processes predictions obtained from Neural Network by finding the product class
with the highest confidence and returning that class' name and associated
confidence in JSON format

Inputs:
Predictions: Array of predictions from Neural Network

Return value:
Dictionary with Max Class and Max Confidence in JSON format
"""
def process_predictions(preds):
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

    return result
