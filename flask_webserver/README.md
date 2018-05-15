## Introduction to Flask Web App

The Flask Web App provides the means to deploy the Predict API that clients can connect to over HTTP. The Predict API accepts an image as an input over HTTP POST, uses the image as input to a trained Neural Network, and returns the classification result in JSON format.

## Components

flask_main.py is the file that runs the web app. This is the file that should be run in a deployment scenario. The file contains standard Flask initialisation code, and then makes several function calls (imported from flask_implementations) that provide the necessary functionality

flask_implementations.py contains the implementation of each function called in flask_main.py.

flask_tests.py contains tests for each of the functions in flask_implementations.py. The main file does not need to be tested because it only contains standard Flask initialisation code and calls to tested functions.

##

How to Run
