import dill as pickle
import json

from flask import Flask,request

app = Flask(__name__)

class Contract:
    def preprocess(self,data):
        img_vect = data["image"]
        return img_vect

    def postprocess(self,data):
        return data

@app.route('/preprocess',methods=['POST'])
def preprocess():
    data = request.form["data"]
    contract = Contract()
    preProcessedData = contract.preprocess(data)
    return preProcessedData

@app.route('/predict',methods=['POST'])
def predict():

    preProcessedData = request.form
    # data is input data for pickel

    modelfile = open('emotion_model.pkl','rb')
    model = pickle.load(modelfile)

    prediction = model.predict(preProcessedData)

    return str(prediction)

@app.route('/postprocess',methods=['POST'])
def postprocess():
    data = request.form["data"]
    contract = Contract()
    postProcessedData = contract.preprocess(data)
    return postProcessedData

@app.route('/healthCheck',methods=['POST'])
def healthCheck():
    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0")