from copyreg import pickle
from flask import Flask, request, jsonify
import numpy as np
import cv2
import tensorflow as tf
from skimage import io
import json
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/predict', methods=['POST'])
def predict():
    links=[]
    zeros=0
    ones=0
    twos=0
    threes=0
    fours=0
    for i in range(1,11):
        path = request.form.get(f'url{i}')
        links.append(path)
        img = io.imread(path,plugin='matplotlib')
        img = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
        clahe = cv2.createCLAHE(clipLimit=10,tileGridSize=(8,8))
        img[:,:,0] = clahe.apply(img[:,:,0])
        img = cv2.cvtColor(img, cv2.COLOR_Lab2RGB)
        bgr = cv2.resize(img, (512,512))
        image = np.array(bgr) / 255.0
        new_model = tf.keras.models.load_model("64x3-CNN.model")
        predict=new_model.predict(np.array([image]))
        per=np.argmax(predict,axis=1)
        if per[0]==0:
            zeros+=1
        elif per[0]==1:
            ones+=1
        elif per[0]==2:
            twos+=1
        elif per[0]==3:
            threes+=1
        elif per[0]==4:
            fours+=1
    return jsonify({"zeros":zeros,"ones":ones,"twos":twos,"threes":threes,"fours":fours})

if __name__=='__main__':
    app.run(debug=True)