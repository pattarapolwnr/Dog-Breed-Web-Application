from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import cv2
import numpy as np
import model

# Importing deps for image prediction
# from tensorflow.keras.preprocessing import image
# from PIL import Image
# import numpy as np
# from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def home():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    return _corsify_actual_response(jsonify({"message": "Hello from backend"}))


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    file = request.files['file']
    file.save('uploads/' + file.filename)

    # Load the image to predict
    img_path = f"./uploads/{file.filename}"
    result, breed = model.yolo(img_path)
    if breed:
        return _corsify_actual_response(jsonify({"message": f"{result} You look like a {breed}."}))
    else:
        return _corsify_actual_response(jsonify({"message": f"{result}"}))


if __name__ == '__main__':
    app.run(debug=True)
