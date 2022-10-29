from encodings import utf_8
from Contract import Contract
import sys

str = ""

str += """import dill as pickle
import json
import random
from flask import Flask,request

app = Flask(__name__)\n\n"""

# contract_file = open('Contract.py','r')
print(sys.argv[1])
contract_file = open(sys.argv[1],'r')
print(type(contract_file),contract_file)
contract_as_string = contract_file.read()
contract_file.close()

str += contract_as_string

str += "\n\n"

str += """@app.route('/preprocess',methods=['POST'])
def preprocess():
    data = request.form[\"data\"]
    contract = Contract()
    preProcessedData = contract.preprocess(data)
    return preProcessedData

@app.route('/predict',methods=['POST'])
def predict():

    preProcessedData = request.form
    # data is input data for pickel

    modelfile = open('"""+sys.argv[2]+"""','rb')
    model = pickle.load(modelfile)

    prediction = model.predict(preProcessedData)

    return str(prediction)

@app.route('/postprocess',methods=['POST'])
def postprocess():
    data = request.form[\"data\"]
    contract = Contract()
    postProcessedData = contract.preprocess(data)
    return postProcessedData

@app.route('/healthCheck',methods=['POST'])
def healthCheck():
    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0")"""

wrapper_class = open('WrapperClass.py','w')
wrapper_class.write(str)
wrapper_class.close()

