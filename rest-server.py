#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
#-------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, send_file, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import pickle
import shutil 
import numpy as np
from search import recommend
import tarfile
import time
from scipy import ndimage
import io
from PIL import Image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
COLLECTION_FILE = './resource/collection.pickle'
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# 调试用代码
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

img_number = 0
relevance = 0.4

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

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 为图库图片链接提供接入点
@app.route('/images/<string:img_name>')
def getDatasetImage(img_name):
    filepath = f"./database/dataset/{img_name}"
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, mimetype="image/jpeg")

@app.route('/history/<string:img_name>')
def getHistoryImage(img_name):
    filepath = f"./uploads/{img_name}"
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, mimetype="image/jpeg")

@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            abort(400)
        
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            print('No selected file')
            abort(400)

        if file is None or file.filename is None or not allowed_file(file.filename):
            print("Invalid file")
            abort(400)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{time.strftime('%Y%m%d_%H%M%S')}.{filename.split('.')[-1]}")
        file.save(filepath)
        # 改用时间命名搜索用的图片，用于历史记录的查询
        result_images = recommend(filepath, extracted_features, img_number, relevance)
        return jsonify({"images": result_images})

@app.route('/newparameters')
def changeSearchParameters():
    if 'number' not in request.args or 'relevance' not in request.args:
        print("Invalid parameter update request")
        abort(400)
    global img_number, relevance
    img_number = int(request.args['number'])
    relevance = (100 - int(request.args['relevance'])) / 100
    return 'hi'

@app.route('/changeCollection', methods = ["GET", "POST"])
def collect():
    print(request.method)
    result = request.files
    if 'image' not in request.args:
        print("Missed image")
        abort(400)
    if 'operation' not in request.args:
        print("Missed operation")
        abort(400)
        #return jsonify({"nothing": "none"})

    if not os.path.exists(COLLECTION_FILE):
        with open(COLLECTION_FILE, 'wb') as f:
            pickle.dump([], f)

    with open(COLLECTION_FILE, 'rb') as f:
        collection = pickle.load(f)
    img = request.args['image']
    if img in collection and request.args['operation'] == 'remove':
        print(f'Remove collection {img}')
        collection.remove(img)
        result = {"operate": "remove"}
    elif request.args['operation'] == 'new':
        print(f'Add collection {img}')
        collection.add(img)
        result = {"operate": "add"}
    with open(COLLECTION_FILE, 'wb') as f:
        pickle.dump(collection, f)
    return jsonify(result)

@app.route('/getCollection')
def getCollection():
    if os.path.exists(COLLECTION_FILE):
        with open(COLLECTION_FILE, 'rb') as f:
            collection = list(pickle.load(f))
    else:
        collection = []
    return jsonify({"collection": collection})

@app.route('/getHistory')
def getHistory():
    if not os.path.exists('./uploads'):
        os.mkdir("uploads")
    history = os.listdir('./uploads/')
    return jsonify({"history": history})

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
    app.run(debug = False, host= '127.0.0.1')
