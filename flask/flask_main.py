import flask_implementations

from flask import Flask, request, jsonify

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

        # Generate location to save file to
        filepath = flask_implementations.generate_unique_filepath('/data/Flask_App/')

        # Save file
        f.save(filepath)

    flask_implementations.crop_image(filepath)

    predictions = flask_implementations.get_predictions()

    output = flask_implementations.process_predictions(predictions)

    return jsonify(output)
