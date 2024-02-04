
import os
from flask import Flask, render_template, redirect, url_for, request,jsonify
from keras.models import load_model
import cv2
from flask import Flask, render_template, redirect, url_for, request,jsonify
import numpy as np
import base64
from PIL import Image
import io
import re

img_size=224

app = Flask(__name__)

model=load_model('model/model-v5.h5')

label_dict={0:'Covid19 Negative', 1:'Covid19 Positive'}

def preprocess(img):

	img=np.array(img)

	if(img.ndim==3):
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	else:
		gray=img

	gray=gray/255
	resized=cv2.resize(gray,(img_size,img_size))
	reshaped=resized.reshape(1,img_size,img_size)
	return reshaped


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/predict", methods=["POST"])
def predict():
	print('HERE')
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image = Image.open(dataBytesIO)

	test_image=preprocess(image)

	prediction = model.predict(test_image)
	result_p = prediction[0][0]
	print(result_p)
	result=np.argmax(prediction,axis=1)[0]
	accuracy=float(np.max(prediction,axis=1)[0])

	label=label_dict[result]

	print(f'Prediction : {prediction}, Result : {result}, Accuracy : {accuracy}')

	response = {'prediction': {'result' : label, 'accuracy' : accuracy}}

	return jsonify(response)

app.run(debug=True)
