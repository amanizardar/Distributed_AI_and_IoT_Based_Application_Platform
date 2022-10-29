from distutils.log import debug
import pickle
import json
import numpy as np
from flask import Flask, request, redirect, url_for, flash, jsonify,render_template,render_template_string
# from PIL import Image

import api

# from io import BytesIO
# from keras.preprocessing import image
# from tensorflow.keras.models import Model
# from tensorflow import keras

# from tensorflow.keras.models import Model
# from tensorflow.keras.applications.inception_v3 import preprocess_input

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def titanic_model():
    return render_template("Corona.html")

@app.route("/callApi", methods=['POST','GET'])
def callApi():
    name = request.form["uname"]
    # male = request.form["male"]
    # female = request.form["female"]
    # Fare = request.form["Fare"]
    # Age = request.form["Age"]
    # Pclass = request.form["Pclass"]
    # Embarked = request.form["Embarked"]
    # sex = int(request.form["sex"])
    # print(request.form,type(request.form)) 

    #print(data,type(data))
    # sensor data
    sensor_data = api.getSensorData("temperature-sensor", 0, "corona_app")#returns float
    print(sensor_data)
    age = int(float(sensor_data))%100+1
    sensor_data = api.getSensorData("temperature-sensor", 0, "corona_app")#returns float
    print(sensor_data)
    sex = int(float(sensor_data))%2
    sensor_data = api.getSensorData("temperature-sensor", 0, "corona_app")#returns float
    print(sensor_data)
    fare = int(float(sensor_data))%500+1
    sensor_data = api.getSensorData("temperature-sensor", 0, "corona_app")#returns float
    print(sensor_data)
    pclass = int(float(sensor_data))%3+1
    sensor_data = api.getSensorData("temperature-sensor", 0, "corona_app")#returns float
    print(sensor_data)
    embarked = int(float(sensor_data))%3+1


    data = {
            "Sex": sex,
            "Fare": fare,
            "Age": age,
            "Pclass": pclass,
            "Embarked": embarked
        }

    print(data)
    response = api.predict(data, "corona_model")
    print(response)
    if response == "[0]":
        response = name + " corona negative"
    else :
        response = name + " corona positive"
    return render_template_string('''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="css url"/>
    </head>
    <body>
        <h1>'''+response+'''</h1>
    </body>
</html>
''')






if __name__ == "__main__":
    app.run()
