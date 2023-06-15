from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf
import env
import helper

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config['UPLOAD_FOLDER'] = "storages"
app.secret_key = "frutify"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/ml")
def ml():
    model = tf.keras.models.load_model(env.fullPath + '\\ml\\ml.h5')
    #model = tf.keras.models.load_model(env.fullPath + '/ml/ml.h5')
    prediction = model.predict([60.0])
    ret = str(prediction)
    return ret


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    file = request.files["image"]
    if "image" not in request.files: return helper.composeReply("ERROR", "Gagal memuat file #1")
    if file.filename == "": return helper.composeReply("ERROR", "Gagal memuat file #2")
    if not (file and helper.allowed_file(file.filename)): 
        return helper.composeReply("ERROR", "Gagal memuat file #3")
    filename = helper.saveFile(file)

    model = tf.keras.models.load_model(env.fullPath + '\\ml\\cnn.h5')
    path = env.fullPath + '\\uploads' + '\\' + filename
    #model = tf.keras.models.load_model(env.fullPath + '/ml/cnn.h5')
    #path = env.fullPath + '/uploads' + '/' + filename

    img = tf.keras.utils.load_img(path, color_mode = 'rgb', target_size = (224, 224, 3), interpolation = 'nearest')
    img = tf.keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    img = img/255.0

    images = np.vstack([img])
    classes = model.predict(images, batch_size = 32)
    predict = np.argmax(classes)
    fruit = "tidak terdefinisi"
    quality = "-"
    precentage = 0.0
    try:
        if classes[0][0]>0.5:
            prediction = 'Fresh Apple'
            fruit = "Apel"
            quality = "Baik"
            precentage = classes[0][0].tolist()

        elif classes[0][1]>0.5:
            prediction = 'Fresh Banana'
            fruit = "Pisang"
            quality = "Baik"
            precentage = classes[0][1].tolist()

        elif classes[0][2]>0.5:
            prediction = 'Fresh Orange'
            fruit = "Jeruk"
            quality = "Baik"
            precentage = classes[0][2].tolist()

        elif classes[0][3]>0.5:
            prediction = 'Rotten Apple'
            fruit = "Apel"
            quality = "Buruk"
            precentage = classes[0][3].tolist()

        elif classes[0][4]>0.5:
            prediction = 'Rotten Banana'
            fruit = "Pisang"
            quality = "Buruk"
            precentage = classes[0][4].tolist()

        elif classes[0][5]>0.5:
            prediction = 'Rotten Orange'
            fruit = "Jeruk"
            quality = "Buruk"
            precentage = classes[0][5].tolist()

    except:
        print("-")

    print(predict)
    print(classes[0])
    print(list(classes[0]))
    print(list(classes[0]).sort())

    data = {
        "filename": filename,
        "fruit": fruit,
        "quality" : quality,
        "precentage" : precentage,
        "classes" : classes[0].tolist(),
        "price_estimation" : 0
    }

    return helper.composeReply("SUCCESS", "prediction", data)


@app.route("/uploads")
def uploads():
    path = request.args.get("path")
    return send_file(env.fullPath + "\\uploads\\" + path)
    #return send_file(env.fullPath + "/uploads/" + path)
    

if __name__ == '__main__':
    app.run(host = env.runHost, port = env.runPort, debug = env.runDebug)
