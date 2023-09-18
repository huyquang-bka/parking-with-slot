import cv2
from flask import Flask, request, jsonify, Response
import requests
import zipfile
import numpy as np

app = Flask(__name__)
port = 5518

# create a black image 1920x1080
original = np.zeros((1080, 1920, 3), np.uint8)
processed = np.zeros((1080, 1920, 3), np.uint8)

data_image = {"original": original, "processed": processed}


def stream(key='original'):
    while True:
        try:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data_image[key] + b'\r\n')
        except:
            pass


@app.route('/original')
def original():
    return Response(stream(key='original'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processed')
def processed():
    return Response(stream(key='processed'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['GET'])
def index():
    ip = requests.get('https://api.ipify.org').content.decode('utf-8')
    return "Connected to Flask server, ip: {}, port: {}".format(ip, port)


@app.route('/get-data', methods=['POST'])
def get_data():
    global original, processed
    f = request.files['file']
    f.save('data.zip')
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall('data')
    try:
        original = cv2.imread('data/original.jpg')
        processed = cv2.imread('data/processed.jpg')
        data_image["original"] = original
        data_image["processed"] = processed
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failed image'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
