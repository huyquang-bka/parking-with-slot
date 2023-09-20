import cv2
from flask import Flask, request, jsonify, Response
import zipfile
import numpy as np
import shutil

app = Flask(__name__)
port = 5518

# create a black image 1920x1080
original_tdn_left = np.zeros((1080, 1920, 3), np.uint8)
processed_tdn_left = np.zeros((1080, 1920, 3), np.uint8)
original_tdn_right = np.zeros((1080, 1920, 3), np.uint8)
processed_tdn_right = np.zeros((1080, 1920, 3), np.uint8)
original_c9 = np.zeros((1080, 1920, 3), np.uint8)
processed_c9 = np.zeros((1080, 1920, 3), np.uint8)
original_d35 = np.zeros((1080, 1920, 3), np.uint8)
processed_d35 = np.zeros((1080, 1920, 3), np.uint8)

data_image = {"original_tdn_left": original_tdn_left,
              "processed_tdn_left": processed_tdn_left,
              "original_tdn_right": original_tdn_right,
              "processed_tdn_right": processed_tdn_right,
              "original_c9": original_c9,
              "processed_c9": processed_c9,
              "original_d35": original_d35,
              "processed_d35": processed_d35
              }


def stream(key='original_tdn_right'):
    while True:
        try:
            fp = key + '.jpg'
            image = cv2.imread(fp)
            if image is not None:
                data_image[key] = image.copy()
        except:
            pass
        ret, buffer = cv2.imencode('.jpg', data_image[key])
        buffer = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')


@app.route('/original-tdn-left')
def original_tdn_left():
    return Response(stream(key='original_tdn_left'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processed-tdn-left')
def processed_tdn_left():
    return Response(stream(key='processed_tdn_left'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/original-tdn-right')
def original_tdn_left():
    return Response(stream(key='original_tdn_right'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processed-tdn-right')
def processed_tdn_left():
    return Response(stream(key='processed_tdn_right'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/original-c9')
def original_c9():
    return Response(stream(key='original_c9'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processed-c9')
def processed_c9():
    return Response(stream(key='processed_c9'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/original-d35')
def original_d35():
    return Response(stream(key='original_d35'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processed-d35')
def processed_d35():
    return Response(stream(key='processed_d35'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"


@app.route('/get-data', methods=['POST'])
def get_data():
    global original_tdn_left, processed_tdn_left
    f = request.files['file']
    fn = f.filename
    f.save(fn)
    with zipfile.ZipFile(fn, "r") as zip_ref:
        zip_ref.extractall()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
