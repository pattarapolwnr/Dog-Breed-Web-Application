from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
import os
import cv2
import numpy as np
import model
import snapchatFilter

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


def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    bg_img = background_img.copy()
    if bg_img.shape[2] == 3:
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    b, g, r, a = cv2.split(img_to_overlay_t)

    mask = cv2.medianBlur(a, 5)

    h, w, _ = img_to_overlay_t.shape
    roi = bg_img[y:y + h, x:x + w]

    if roi.shape[0] == h and roi.shape[1] == w:
        img1_bg = cv2.bitwise_and(
            roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(
            img_to_overlay_t, img_to_overlay_t, mask=mask)

        bg_img[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

    return bg_img


# cap = cv2.VideoCapture(0)
prev_nose_x, prev_nose_y = 0, 0
prev_mouth_x, prev_mouth_y = 0, 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

ears_img = cv2.imread('snapchatFilter/ears.png', -1)
nose_img = cv2.imread('snapchatFilter/nose.png', -1)
mouth_img = cv2.imread('snapchatFilter/mouth.png', -1)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            noses = nose_cascade.detectMultiScale(roi_gray, 1.3, 5)
            for (nx, ny, nw, nh) in noses:
                frame = overlay_transparent(
                    frame, nose_img, x + nx, y + ny, (nw, nh))

            mouths = mouth_cascade.detectMultiScale(roi_gray, 1.8, 20)
            for (mx, my, mw, mh) in mouths:
                overlay_width = mw
                overlay_height = mh
                overlay_x = x + mx + mw // 2 - overlay_width // 2
                overlay_y = y + my + mh - 25

                frame = overlay_transparent(
                    frame, mouth_img, overlay_x, overlay_y, (overlay_width, overlay_height))

            # overlay ears
            frame = overlay_transparent(
                frame, ears_img, x, y - h//5, (w, h//3))
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # for frame in camera.get_frame():
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
