from flask import Flask, render_template, url_for, request, jsonify
from recognition.predict import Predict
import cv2
import base64
import numpy as np
import io
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/_display')
def display_str():
    base64 = []
    for i in range(7):
        num = 'num' + str(i)
        base64.append(request.args.get(num, '', type=str))
    
    zip_code = ''
    for data in base64:
        zip_code += getNumber(data)
    result = get_address(zip_code)
    result['zip_code'] = zip_code
    return jsonify(result)


# refer to https://qiita.com/TsubasaSato/items/908d4f5c241091ecbf9b
def getNumber(base64_data):
    img_binary = base64.b64decode(base64_data[23:])
    jpg = np.frombuffer(img_binary, dtype=np.uint8)

    img = cv2.imdecode(jpg, cv2.IMREAD_GRAYSCALE)

    predict = Predict()
    result = predict.predict(img)

    return str(result)


def get_address(zip_code):
    url = 'https://api.zipaddress.net/?zipcode=%s' % zip_code
    res = requests.get(url)
    data = res.json()
    return data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
