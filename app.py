import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

from keras.models import load_model

import base64
from PIL import Image
import cv2
import io

st.title('Diagnostic of COVID-19 Pneumonia through Convolutional Neural Networks Using Chest X-RAY')
st.markdown('## This is not suitable for diagnostic purpose ')
st.markdown('### This is done for education purpose ')
st.markdown('# Do not used this as diagnostic purpose \n # Always keep touch with medical practitioner')

result=0

img_size=224

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

def predict(image):

	test_image=preprocess(image)

	prediction = model.predict(test_image)
	result_p = prediction[0][0]
	print(result_p)
	result=np.argmax(prediction,axis=1)[0]
	accuracy=float(np.max(prediction,axis=1)[0])

	label=label_dict[result]

	print(f'Prediction : {prediction}, Result : {result}, Accuracy : {accuracy}')
	st.write(f' Result : {label_dict[result]}, Accuracy : {accuracy}')


# Display file uploader widget
uploaded_file = st.file_uploader("Upload a chest x ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
	predict(Image.open(uploaded_file))

if uploaded_file is not None:
    # Open the uploaded image file
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)
else:
    st.write("Upload an image file.")
