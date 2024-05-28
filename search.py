################################################################################################################################
# This function implements the image search/retrieval .
# inputs: Input location of uploaded image, extracted vectors
# 
################################################################################################################################
import tensorflow.compat.v1 as tf
import numpy as np
import os
from scipy import ndimage
from scipy.spatial.distance import cosine
from sklearn.neighbors import NearestNeighbors
import pickle 
import os
from tempfile import TemporaryFile
from tensorflow.python.platform import gfile
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
BOTTLENECK_TENSOR_SIZE = 2048
MODEL_INPUT_WIDTH = 299
MODEL_INPUT_HEIGHT = 299
MODEL_INPUT_DEPTH = 3
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
RESIZED_INPUT_TENSOR_NAME = 'ResizeBilinear:0'
MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M

def get_top_k_similar(image_data, pred, pred_final, k, relevance=0.40):
    print("total data",len(pred))
    print(image_data.shape)
    
    # cosine calculates the cosine distance, not similiarity. Hence no need to reverse list
    print(k)
    top_k_ind = np.argsort([cosine(image_data, pred_row)
        for _, pred_row in enumerate(pred)
        if cosine(image_data, pred_row) < relevance])
    if k != 0:
        top_k_ind = top_k_ind[:k]
    print(top_k_ind)
    
    result_images = [
        f"/images/{os.path.split(pred_final[neighbor])[1]}" for neighbor in top_k_ind
    ]
    return result_images

                
def create_inception_graph():
  """"Creates a graph from saved GraphDef file and returns a Graph object.

  Returns:
    Graph holding the trained Inception network, and various tensors we'll be
    manipulating.
  """
  with tf.Session() as sess:
    model_filename = os.path.join(
        'imagenet', 'classify_image_graph_def.pb')
    with gfile.FastGFile(model_filename, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      bottleneck_tensor, jpeg_data_tensor, resized_input_tensor = (
          tf.import_graph_def(graph_def, name='', return_elements=[
              BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME,
              RESIZED_INPUT_TENSOR_NAME]))
  return sess.graph, bottleneck_tensor, jpeg_data_tensor, resized_input_tensor

def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(
        bottleneck_tensor,
        {image_data_tensor: image_data}
    )
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values

# 约定 img_number 为 0 时不对结果数量进行限制
def recommend(imagePath, extracted_features, img_number=0, relevance=0.40):
    tf.reset_default_graph()

    config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )

    sess = tf.Session(config=config)
    graph, bottleneck_tensor, jpeg_data_tensor, resized_image_tensor = (create_inception_graph())
    image_data = gfile.FastGFile(imagePath, 'rb').read()
    features = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)	

    with open('neighbor_list_recom.pickle','rb') as f:
        neighbor_list = pickle.load(f)
    print("loaded images")

    return get_top_k_similar(features, extracted_features, neighbor_list, img_number, relevance=relevance)

