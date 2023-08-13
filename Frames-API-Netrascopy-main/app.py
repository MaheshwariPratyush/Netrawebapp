from flask import Flask, request, jsonify
import cv2
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from ast import For
from pickle import TRUE
from re import I

app = Flask(__name__)

# Cloudinary config
cloudinary.config( 
  cloud_name = "woofyverse", 
  api_key = "812158734764712", 
  api_secret = "aG5zKoQB1iX2tnqZVfmUsqVOKNU" 
)

config = cloudinary.config(secure=TRUE)

@app.route('/')
def home():
    return "Hello World"

@app.route('/generate',methods=['POST'])
def generate():
    path = request.form.get('url')
    cam = cv2.VideoCapture(path)

    try:
        # creating a folder named data
        if not os.path.exists('./data'):
            os.makedirs('./data')
    
    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')
    
    # frame
    list=[]
    currentframe = 0
    i=0
    while(i<11):
        
        # reading from frame
        ret,frame = cam.read()
    
        if ret:
            # if video is still left continue creating images
            # save frame
            name = './data/' + str(i) + '.jpg'
            result = cloudinary.uploader\
            .upload(name)
            print ('Uploading...' + name)
            url= result.get("url")
            list.append(url)
            i=i+1
            # writing the extracted images
            cv2.imwrite(name, frame)
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 24 # i.e. at 30 fps, this advances one second
            cam.set(1, currentframe)
        else:
            break
    return jsonify(list)
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    app.run(debug=True)
