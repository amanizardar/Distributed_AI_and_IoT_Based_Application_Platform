from flask import Flask, session, request, render_template, make_response, redirect
import requests
import cgi, os
import json
import jwt
import ast
import cgitb; cgitb.enable()
from pymongo import MongoClient
import certifi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

AUTHENTICATION_MANAGER = 'http://127.0.0.1:5001'
MODEL_APP_REPO = 'http://127.0.0.1:5002'
DEPLOYER = "http://127.0.0.1:5005"
SCHEDULER = "http://127.0.0.1:5010"
SCHBACK = "http://127.0.0.1:5011"

SENSOR_CONFIGURER = "http://127.0.0.1:6001"
APP_CONFIGURER = "http://127.0.0.1:6005"

AUTH_URL = AUTHENTICATION_MANAGER + '/authenticate_user/'
CREATE_URL = AUTHENTICATION_MANAGER + '/create_user/'


CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

dbname = client['Application']
app_req_db = dbname["app_requirement"]



@app.route('/')
def home():
   return render_template('index.html')

@app.route('/signin', methods = ['POST'])
def signin_page():
    user_type = request.form['user_type']
    return render_template('signin_page.html',user_type =  user_type, authcode="None",mesg="")

def session_expired(user_type,msg):
    message = "Session Expired! Please Login Again."
    if msg != "":
        message = msg 
    response = make_response(render_template('signin_page.html', user_type =  user_type, authcode="error_login", mesg = message))
    response.set_cookie('auth_token', "")
    return response

@app.route('/Dashboard/<user_type>', methods = ['GET','POST'])
def dashboard(user_type, auth_token ="" ):
  
    if auth_token == "":
        auth_token = request.headers.get('Authorization')
        if auth_token == None:
            auth_token = request.cookies.get('auth_token')
 
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
    except:
        return session_expired(user_type,'')
    
    to_send={}
    #to_send["auth_token"] = auth_token
    to_send["username"] = payload['sub']

    # response = requests.post(MODEL_APP_REPO + '/get_models',json=to_send).content.decode()
    # model_list = response.split()
    if user_type == "Platform_Configurer":
        response = make_response(render_template("configurer.html",URL = SENSOR_CONFIGURER,username= payload['sub'], token = auth_token,user_type=user_type))
    elif user_type == "End_User":
        ########################
        apps_list = list(app_req_db.find())
        app_names = []
        app_ids = []

        for app_instance in apps_list:
            app_names.append(app_instance['app_name'])
            app_ids.append(app_instance['app_id'])

        response = make_response(render_template("choose_app.html", app_names=app_names, app_ids=app_ids))
        #response = make_response(render_template("choose_app.html",URL = APP_CONFIGURER,user_type=user_type))
    else:
        response = make_response(render_template("dashboard.html",user_type=user_type,DEPLOYER = DEPLOYER))
    # if user_type == "Data_Scientist":
    #     response = make_response(render_template("data_sci_dashboard.html",response = model_list))
    #     response = make_response(render_template("data_sci_dashboard.html"))
    # elif user_type == "App_Developer":
    #     app_list = requests.post(MODEL_APP_REPO + '/get_all_models',json=to_send).content.decode().split()
    #     response = make_response(render_template("app_dev_dashboard.html",response = response, response2 = app_list , username=payload['sub']))

    response.set_cookie('auth_token', auth_token)
    return response 
    #return requests.post(SCHEDULER_ADDRESS,headers={'Authorization': session["auth_token"]},json={'username':username,'role':role})

SENSOR_INSTANCES_DB = client['sensor']["SENSOR_INSTANCES"]
given_app_id = "app1"
app_sensor_data = {}
sensor_kinds = list()
sensor_count = list()

def processRequest(appSensorReq):
    # print(appSensorReq)
    sensorInstances = list(SENSOR_INSTANCES_DB.find())
    binding_map = list()        # type + location + count : id
    alotted_sensors = {}        # type + location : count_alotted
    busy_sensor_map = [0] * len(sensorInstances)


    for i in appSensorReq['info']:
        currentSensorReq = i['type'] + i['location']
        sensorAvailable = False

        for j in range(len(sensorInstances)):   
            if sensorInstances[j]['type'] == i['type'] and sensorInstances[j]['location'] == i['location'] and busy_sensor_map[j] == 0:
                busy_sensor_map[j] = 1
                count = alotted_sensors.get(currentSensorReq, 0)
                alotted_sensors[currentSensorReq] = count+1

                key = currentSensorReq + str(count)
                # print(key)
                topic_id =str(sensorInstances[j]['_id'])+"_topic"
                val = {"type": sensorInstances[j]['type'] , "location" : sensorInstances[j]['location'], "topic" : topic_id}
                binding_map.append(val)
                sensorAvailable = True
                break

        if not sensorAvailable:
            print("Error: Sensor not available!")
            return
    # print(binding_map)
    return binding_map

@app.route("/jsonifyRequest", methods=['POST', 'GET'])
def sensor_requirements1():
    auth_token = request.cookies.get('auth_token')
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print(auth_token)
    print("+++++++++++++++++++++++++++++++++++++++++++")
    request_details = {"info" : list()}
    new_sensor_instance = request.form.to_dict()
    # print(new_sensor_instance)
    for each in new_sensor_instance:
        l = each.split('_')
        # print (l)
        val = {"type" : l[0] , "location" : new_sensor_instance[each]}
        request_details["info"].append(val)

    # print(request_details)
    
    binding_map = processRequest(request_details)
    scheduling_data = {"app_id": given_app_id,"info" : binding_map}
    # print(scheduling_data)
    response=requests.post(SCHBACK+"/schedule_data",json=scheduling_data).content.decode()
    
    return render_template("temp.html",user_type="End_User",token=auth_token,URL=SCHBACK)
    # return render_template("scheduler_frontend.html",URL = SCHBACK)


@app.route("/sensor_location", methods=['POST', 'GET'])
def sensor_requirements():
    app_sensor_data = {}
    sensor_kinds = list()
    sensor_count = list()

    selectedApp = request.form.to_dict()

    for i in selectedApp:
        given_app_id = i
        print(i)

    sensors_req = list(app_req_db.find())

    for app_instance in sensors_req:
        if app_instance["app_id"] == given_app_id:
            app_sensor_data = app_instance

    if app_sensor_data == {}:
        print("Error : App ID not found")
    else:
        print("Application sensor requirements are : ",
              app_sensor_data["sensors"])

    app_sensor_req = ast.literal_eval(app_sensor_data["sensors"])

    for sensor_type in app_sensor_req:
        sensor_kinds.append(sensor_type)
        sensor_count.append(app_sensor_req[sensor_type])

    return render_template("sensor_location.html", sensor_kinds=sensor_kinds, sensor_count=sensor_count)

@app.route('/register/<user_type>', methods = ['POST'])
def register(user_type):
    username=request.form['username']
    password=request.form['password']
    response = requests.post(CREATE_URL+user_type,json={'username':username,'password':password}).content.decode()
    payload = json.loads(response)
    if(payload["message"]=="Success"):
        return dashboard(user_type, payload['auth_token']);    
    else:
        return render_template('signin_page.html', user_type =  user_type, authcode="error_signup", mesg = payload["message"])


@app.route('/login/<user_type>', methods = ['POST'])
def login(user_type):
    username=request.form['username']
    password=request.form['password']
    response = requests.post(AUTH_URL+user_type,json={'username':username,'password':password}).content.decode()
    payload = json.loads(response)
    if(payload["message"]=="Success"):
        return dashboard(user_type, payload['auth_token']);    
    else:
        return render_template('signin_page.html', user_type =  user_type, authcode="error_login", mesg = payload["message"])


@app.route('/Upload/<user_type>', methods = ['POST'])
def upload(user_type):
    auth_token = request.cookies.get('auth_token')
    # user_type = ""
    # if type == "App":
    #     user_type = 'App_Developer' 
    # else:
    #     user_type = 'Data_Scientist' 
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
        username = payload['sub']
        #f = request.files['filename']
        file_label = ['f1','f2','f3','f4','f5','f6']
        f=[]
        f.append(request.files['f1'])
        f.append(request.files['f2'])
        f.append(request.files['f3'])
        f.append(request.files['f4'])
        f.append(request.files['f5'])
        f.append(request.files['f6'])
        files = []
        for file,label in zip(f,file_label):
            files.append((label, (file.filename, file.read(), file.content_type)))
        
        to_send={}
        to_send["username"]=username
        to_send["role"]=user_type
        response=requests.post(DEPLOYER+'/submit',json=to_send,files=files).content.decode()
        # if user_type == 'App_Developer':
        #     to_send["app_name"]=f.filename
        #     f.save(os.path.join("./Data/Model/", f.filename))
        #     response=requests.post(MODEL_APP_REPO+'/add_app',json=to_send).content.decode()
        # else:
        #     to_send["model_name"]=f.filename
        #     f.save(os.path.join("./Data/App/", f.filename))
        #     response=requests.post(MODEL_APP_REPO+'/add_model',json=to_send).content.decode()
        if response == "ok":
            dashboard(user_type,auth_token)
            #return render_template("temp.html",username=username,user_type=user_type,token=auth_token,URL=SCHBACK)
        else:
            return "error"
    except Exception as e:
        return session_expired(user_type,str(e))



if(__name__ == '__main__'):
    app.run(host ='127.0.0.1',port=5000,debug=True)