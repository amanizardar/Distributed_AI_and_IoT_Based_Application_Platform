import pickle
import json
import numpy as np
from flask import Flask, request, redirect, url_for, flash, jsonify

app = Flask(__name__)


@app.route("/titanic_model", methods=['POST'])
def titanic_model():
    data = request.json
    temp = []

    for key in data.keys():
        temp.append(data[key])

    data = np.array(temp).reshape((1, 5))

    model_file = open("data_scientist/titanic_model.pkl", 'rb')
    loaded_model = pickle.load(model_file)

    result = loaded_model.predict(data)[0]

    return str(result)


@app.route("/salary_model", methods=['POST'])
def salary_model():
    data = request.json
    temp = []

    for key in data.keys():
        temp.append(data[key])

    data = np.array(temp).reshape((1, 1))

    model_file = open("data_scientist/salary_model.pkl", 'rb')
    loaded_model = pickle.load(model_file)

    result = loaded_model.predict(data)[0]

    return str(result)


@app.route("/sales_model", methods=['POST'])
def sales_model():
    data = request.json
    temp = []

    for key in data.keys():
        temp.append(data[key])

    data = np.array(temp).reshape((1, 3))

    model_file = open("data_scientist/sale_model.pkl", 'rb')
    loaded_model = pickle.load(model_file)

    result = loaded_model.predict(data)[0]

    return str(result)


@app.route("/wine_model", methods=['POST'])
def wine_model():
    data = request.get_json()

    model_file = open("data_scientist/wine_model.pkl", 'rb')
    loaded_model = pickle.load(model_file)

    result = loaded_model.predict(data)

    return str(result[0])


if __name__ == "__main__":
    app.run(port=8080, debug=True)
