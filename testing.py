import os
import sys

current_location = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(current_location, 'vendored'))

import tensorflow as tf  
import numpy as np


        
def get_model(model_dir,img):
    model = tf.saved_model.load(model_dir)
    print("model-loded")
    gan_model = model.signatures["serving_default"]
    scores = gan_model((img))
    return scores['conv2d_18'][0,:,:,:]


def model_predict(image, upload_path):
    img = tf.io.read_file(image)
    img = tf.image.decode_png(img,channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [128, 128])
    img = tf.expand_dims(img,axis=0)
    pred = get_model('tmp',img)
    pred = tf.image.convert_image_dtype(pred, tf.uint8)
    pred = tf.image.encode_png(pred)
    tf.io.write_file(upload_path,pred,name=None)
    
     
def handler(filename):
	download_path = filename
	upload_path = "images/1.png"
	model_predict(download_path, upload_path)
        

