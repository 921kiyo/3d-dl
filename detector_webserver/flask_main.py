import flask_implementations

from flask import Flask, request, jsonify

import numpy as np

import keras

# from keras.models import load_model

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

from keras_retinanet import models
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import (
    read_image_bgr,
    preprocess_image,
    resize_image,
)

import os
import numpy as np
import train_keras_retinanet as ret

import json


# Change this to location of your model
model = models.load_model('/data/g1753002_ocado/manhattan_project/trained_models/retinanet_second_attempt/resnet50_csv_150_inf.h5', backbone_name='resnet50')

# Change this to preferred location
# This is where HTTP attachments are stored
UPLOAD_FOLDER = '/vol/project/2017/530/g1753002/Flask_App/'

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
Flask route binding for web server

The web app can now be accessed by submitting a HTTP POST request
to <hostname>/api

"""
@app.route('/detector', methods=['POST'])
def predict_api():
    # Save image uploaded using HTTP POST Request
    print("[INFO] loading and pre-processing image...")
    if request.method == 'POST':
        f = request.files['my_image']

        # Generate new location to save file to
        # Function argument is the path to save to, change this as required
        filepath = flask_implementations.generate_unique_filepath('/data/Flask_App/')

        # Save file
        f.save(filepath)

    flask_implementations.crop_image(filepath)

    detections = flask_implementations.get_predictions(filepath, model)

    scores, labels, boxes = detections

    items = []

    for score, label, box in zip(scores, labels, boxes):
        current = []

        current.append(label)

        cmin, rmin, cmax, rmax = box

        current.append(cmin)
        current.append(rmin)
        current.append(cmax)
        current.append(rmax)

        current.append(score)

        items.append(current)


    # detections = np.array(detections).tolist()

    return json.dumps(items)
