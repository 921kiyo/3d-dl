import flask_implementations

from flask import Flask, request, jsonify

import numpy as np

from keras.models import load_model

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

# Change this to location of your model
model = load_model('/data/g1753002_ocado/manhattan_project/trained_models/first_attempt_with_all_layers_unfrozen/model.h5')

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
@app.route('/api', methods=['POST'])
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

    predictions = flask_implementations.get_predictions(filepath, model)

    output = flask_implementations.process_predictions(predictions)

    return jsonify(output)
