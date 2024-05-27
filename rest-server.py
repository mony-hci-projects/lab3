#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
#-------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, send_file, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from scipy.sparse import base
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
import io
from PIL import Image
#from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
RESULT = 'static/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")#, static_folder="./vue-template/dist")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((10000,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i,line in enumerate(f):
        extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================

# 具体作用见 search.py 的 get_top_k_similar 函数
current_img_map = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    #result = 'static/result'
    if not gfile.Exists(RESULT):
          os.mkdir(RESULT)
    shutil.rmtree(RESULT)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            current_img_map, result_images = recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            image_list = [os.path.join(image_path, file)
                for file in os.listdir(RESULT)
                if not file.startswith('.')]
            images = { 'images': [] }
            for image in image_list:
                images['images'].append(image)
            #return jsonify(images)
            return jsonify({"images": result_images})

@app.route('/images/<string:img_name>')
def getDatasetImage(img_name):
    return send_file(f"./database/dataset/{img_name}", mimetype="image/jpeg")
    #img_stream = ''
    #with open(f"./database/dataset/{img_name}", 'rb') as img:
    #    img_stream = img.read()
    #    img_stream = base64.b64encode(img_stream).decode()
    #return img_stream

@app.route('/collect', methods = ["GET", "POST"])
def collect():
    print(request.method)
    result = request.files
    if 'image' not in request.args:
        print("Missed image")
        return redirect(request.url)
    img = request.args['image']
    print(img)
    result = {img: img}
    return jsonify(result)

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                       	            #						     									       
#                                                                                                                              
#==============================================================================================================================
@app.route("/")
def main():
    return app.send_static_file("index.html")
    #return render_template("main.html")   

if __name__ == '__main__':
    #app.run(debug = True, host= '127.0.0.1')
    #app.run(debug = False, host= '127.0.0.1')
    app.run(debug = False, host= '100.80.16.122')
