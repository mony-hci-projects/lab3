#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
#-------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, abort, request, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import pickle
import numpy as np
from search import recommend
import time
import io
from PIL import Image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
COLLECTION_FILE = './resource/collection.pickle'
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "", static_folder="./vue-template/dist/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# 调试用代码，用于热重载前端代码
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

# 搜索时使用的相关属性
img_number = 0
relevance = 0.4

#================================#
#                                #
# 加载图片检索所需的提取特征向量 #
#                                #
#================================#
extracted_features=np.zeros((10000,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i,line in enumerate(f):
        extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#========================#
#                        #
# 检索系统所需的辅助函数 #
#                        #
#========================#

# 检查是否是支持的文件格式
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

# 为历史记录图片提供接入点
@app.route('/history/<string:img_name>')
def getHistoryImage(img_name):
    filepath = f"./{app.config['UPLOAD_FOLDER']}/{img_name}"
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, mimetype="image/jpeg")

#==================#
#                  #
# 图片检索相关实现 #
#                  #
#==================#

@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            if request.args['image']:
                return requery(request.args['image'])
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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                f"{time.strftime('%Y%m%d_%H%M%S')}.{filename.split('.')[-1]}")
        file.save(filepath)
        # 改用时间命名搜索用的图片，用于历史记录的查询
        result_images = recommend(filepath, extracted_features, img_number, relevance)
        return jsonify({"images": result_images})

# 用于使用历史记录进行查询
def requery(image_name):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if not os.path.exists(filepath):
        abort(404)
    result_images = recommend(filepath, extracted_features, img_number, relevance)
    return jsonify({"images": result_images})

# 更新检索使用的相关参数
@app.route('/newparameters')
def changeSearchParameters():
    if 'number' not in request.args or 'relevance' not in request.args:
        print("Invalid parameter update request")
        abort(400)
    global img_number, relevance
    img_number = int(request.args['number'])
    relevance = (100 - int(request.args['relevance'])) / 100
    return 'hi'

#==================#
#                  #
# 辅助功能相关实现 #
#                  #
#==================#

# 新增/删除收藏
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

# 获取收藏图片
@app.route('/getCollection')
def getCollection():
    if os.path.exists(COLLECTION_FILE):
        with open(COLLECTION_FILE, 'rb') as f:
            collection = list(pickle.load(f))
    else:
        collection = []
    return jsonify({"collection": collection})

# 获取历史记录
@app.route('/getHistory')
def getHistory():
    if not os.path.exists(f'./{app.config["UPLOAD_FOLDER"]}'):
        os.mkdir(app.config["UPLOAD_FOLDER"])
    history = os.listdir(app.config["UPLOAD_FOLDER"])
    return jsonify({"history": history})

# 删除历史记录
@app.route('/removeHistory')
def removeHistory():
    print(request.method)
    result = request.files
    if 'image' not in request.args:
        print("Missed image")
        abort(400)

    img = request.args['image']
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.mkdir(app.config["UPLOAD_FOLDER"])

    if not os.path.exists(f'./{app.config["UPLOAD_FOLDER"]}/{img}'):
        abort(304)
    else:
        os.remove(f'./{app.config["UPLOAD_FOLDER"]}/{img}')
        return getHistory()

#========#
#        #
# 主函数 #
#        #
#========#

# 各界面挂载至 index.html，后续由 vue-router 进行路由
@app.route("/")
@app.route("/history")
@app.route("/collection")
@app.route("/advance")
def main():
    return app.send_static_file("index.html")

if __name__ == '__main__':
    #app.run(debug = True, host= '127.0.0.1')
    app.run(debug = False, host= '127.0.0.1')
