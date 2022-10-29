from flask import Flask, request, render_template
import threading
from flask import flash
from pymongo import MongoClient
import schedule
import time
import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("temp.html")

def renderUI():
    app.use_reloader=False
    app.run(port=5011,debug=True)

renderUI()
