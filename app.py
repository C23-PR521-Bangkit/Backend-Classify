from flask import Flask
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import env

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config['UPLOAD_FOLDER'] = "storages"
app.secret_key = "frutify"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/ml")
def ml():
    model = tf.keras.models.load_model('D:\\BANGKIT\\backend_classify\\ml\\ml.h5')
    prediction = model.predict([60.0])
    ret = str(prediction)
    return ret

@app.route("/cnn", methods=['POST'])
def cnn():
    model = tf.keras.models.load_model('D:\\BANGKIT\\backend_classify\\ml\\cnn.h5')
    
    path = 'D:\\BANGKIT\\backend_classify\\uploads\\apple2.jpg'
    imgx = plt.imread(path)

    img = tf.keras.utils.load_img(path, target_size=(224, 224))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x/255.0

    images = np.vstack([x])
    classes = model.predict(images, batch_size=32)
    print(classes)
    if classes[0][0]>0.5:
        prediction = 'apel busuk'
    elif classes[0][1]>0.5:
        prediction = 'apel segar'
    elif classes[0][2]>0.5:
        prediction = 'jeruk busuk'
    elif classes[0][3]>0.5:
        prediction = 'jeruk segar'
    elif classes[0][4]>0.5:
        prediction = 'mangga busuk'
    elif classes[0][5]>0.5:
        prediction = 'mangga segar'
    elif classes[0][6]>0.5:
        prediction = 'pisang busuk'
    elif classes[0][7]>0.5:
        prediction = 'pisang segar'
    elif classes[0][8]>0.5:
        prediction = 'stroberi busuk'
    elif classes[0][9]>0.5:
        prediction = 'stroberi segar'

    ret = str(prediction)
    return ret

if __name__ == '__main__':
    app.run(host = env.runHost, port = env.runPort, debug = env.runDebug)
