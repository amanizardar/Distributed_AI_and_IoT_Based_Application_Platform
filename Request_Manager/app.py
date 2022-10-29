from flask import Flask, session, request, render_template, make_response, redirect
import requests
import cgi, os
import json
import jwt
import ast
import cgitb

import cgitb; cgitb.enable()
from pymongo import MongoClient
import certifi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

is_local = False

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
ip_dbname = client['AI_PLATFORM']
IP_ADDRESSES = ip_dbname["MODULE_URL"]

REQUEST_MANAGER = 'http://127.0.0.1:5000'
AUTHENTICATION_MANAGER = 'http://127.0.0.1:5001'
MODEL_APP_REPO = 'http://127.0.0.1:5002'
DEPLOYER = "http://127.0.0.1:5005"
SCHEDULER = "http://127.0.0.1:5011"
SCHBACK = "http://127.0.0.1:5011"
SLCM = ""
SENSOR_CONFIGURER = "http://127.0.0.1:6001"
APP_CONFIGURER = "http://127.0.0.1:6005"
SENSOR_BINDER = "http://127.0.0.1:6005"





# SCHBACK = IP_ADDRESSES.find_one({'name': 'Scheduler'})['url']

# APP_CONFIGURER = IP_ADDRESSES.find_one({'name': 'Sensor_Binder'})['url']


# for i in ip_table:
#     if 'REQUEST_MANAGER' in i:
#         REQUEST_MANAGER = i['REQUEST_MANAGER']
#     if 'AUTHENTICATION_MANAGER' in i:
#         AUTHENTICATION_MANAGER = i['AUTHENTICATION_MANAGER']
#     if 'MODEL_APP_REPO' in i:
#         MODEL_APP_REPO = i['MODEL_APP_REPO']
#     if 'DEPLOYER' in i:
#         DEPLOYER = i['DEPLOYER']
#     if 'SCHBACK' in i:
#         SCHBACK = i['SCHBACK']
#     if 'SENSOR_CONFIGURER' in i:
#         SENSOR_CONFIGURER = i['SENSOR_CONFIGURER']
#     if 'APP_CONFIGURER' in i:
#         APP_CONFIGURER = i['APP_CONFIGURER']
#     if 'SENSOR_BINDER' in i:
#         SENSOR_BINDER = i['SENSOR_BINDER']
#     if 'SCHEDULER' in i:
#         SCHEDULER = i['SCHEDULER']


dbname = client['AI_PLATFORM']
app_req_db = dbname["app_requirement"]
users_apps = dbname["app_user_node"]
app_node=dbname["app_nodes"]
model_node=dbname["model_nodes"]
sensor_node=dbname["SENSOR_INFO"]
mode_node=dbname["model_users"]
@app.route('/')
def home():
   return render_template('index.html')

@app.route("/logout")
def logout():
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
    DEPLOYER = "http://127.0.0.1:5005"
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
    username = payload['sub']
    # response = requests.post(MODEL_APP_REPO + '/get_models',json=to_send).content.decode()
    # model_list = response.split()
    if user_type == "Platform_Configurer":
        SENSOR_CONFIGURER = "http://127.0.0.1:6001"
        SLCM = "http://127.0.0.1:8000"
        if not is_local:
            SLCM = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
            SENSOR_CONFIGURER = IP_ADDRESSES.find_one({'name': 'Sensor_Manager'})['url']
        response = make_response(render_template("configurer.html",SLCM_URL = SLCM, URL = SENSOR_CONFIGURER,username= payload['sub'], token = auth_token,user_type=user_type))
    
    elif user_type == "End_User":
        apps_list = list(app_req_db.find())
        app_names = []
        app_ids = []

        for app_instance in apps_list:
            app_names.append(app_instance['app_name'])
            app_ids.append(app_instance['app_id'])

        username = payload['sub']
        sche_apps = []
        sche_app_urls = []

        for i in list(users_apps.find()):
            if i['enduser'] == username:
                sche_apps.append(i['app'])
                url = "http://"+  i['ip']+':'+str(i['port'])
                sche_app_urls.append(url)

        for i in range(len(app_names)):
            if app_names[i] in sche_apps:
                app_names.pop(i)
                app_ids.pop(i)

        response = make_response(render_template("choose_app.html", sche_apps = sche_apps, sche_app_urls = sche_app_urls, app_names=app_names, app_ids=app_ids))
        #response = make_response(render_template("choose_app.html",URL = APP_CONFIGURER,user_type=user_type))
    else:
        mode_node.insert_many([{"model":"m1", "uname":"Ammu", },
                       {"model":"m2", "uname":"Priya"}])
        all_model_list=model_node.find({})
        print("hello")
        print(username)
        ds_model_list=mode_node.find({"uname":username})
        sensor_list=sensor_node.find({})
        print(ds_model_list)
        # mode_nodes=mode_node
        # print(all_model_list)
        # print(all_model_list)
        # print(sensor_list)
        l=[]
        # for each in ds_model_list:
        #     # l.append(each['model'])
        #     print("This is Aman")
        #     print(each['model'])
        # print(l)
        response = make_response(render_template("dashboard.html",user_type=user_type,username=username,DEPLOYER = DEPLOYER,ds_model_list=ds_model_list,all_model_list=all_model_list,sensor_list=sensor_list ))
        #response = make_response(render_template("dashboard.html",user_type=user_type,DEPLOYER = DEPLOYER))
    # if user_type == "Data_Scientist":
    #     response = make_response(render_template("data_sci_dashboard.html",response = model_list))
    #     response = make_response(render_template("data_sci_dashboard.html"))
    # elif user_type == "App_Developer":
    #     app_list = requests.post(MODEL_APP_REPO + '/get_all_models',json=to_send).content.decode().split()
    #     response = make_response(render_template("app_dev_dashboard.html",response = response, response2 = app_list , username=payload['sub']))

    response.set_cookie('auth_token', auth_token)
    return response 
    #return requests.post(SCHEDULER_ADDRESS,headers={'Authorization': session["auth_token"]},json={'username':username,'role':role})

@app.route("/sensor_location/", methods=['POST', 'GET'])
def sensor_requirements():
    SCHEDULER = "http://127.0.0.1:5011"
    SENSOR_BINDER = "http://127.0.0.1:6005"

    user_type = "End_User"
    auth_token=''
    if auth_token == "":
        auth_token = request.headers.get('Authorization')
    if auth_token == None:
        print("hellow")
        auth_token = request.cookies.get('auth_token')
    
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
    except:
        return session_expired(user_type,'')

    app_sensor_data = {}
    sensor_kinds = list()
    sensor_count = list()

    selectedApp = request.form.to_dict()

    error = ""
    for i in selectedApp:
        given_app_id = i

    print(given_app_id)
    sensors_req = list(app_req_db.find())

    for app_instance in sensors_req:
        if app_instance["app_id"] == given_app_id:
            app_sensor_data = app_instance

    print(app_sensor_data)    

    try:
        print("Application sensor requirements are : ",
            app_sensor_data["sensors"])
    except:
        error = "Not Enough Sensors!"
        given_app_id = request.form.to_dict()["given_app_id"]
        for app_instance in sensors_req:
            if app_instance["app_id"] == given_app_id:
                app_sensor_data = app_instance
        print("Application sensor requirements are : ",
            app_sensor_data["sensors"])


    app_sensor_req = ast.literal_eval(app_sensor_data["sensors"])

    for sensor_type in app_sensor_req:
        sensor_kinds.append(sensor_type)
        sensor_count.append(app_sensor_req[sensor_type])
    if not is_local:
        SENSOR_BINDER = IP_ADDRESSES.find_one({'name': 'Sensor_Binder'})['url']
        SCHEDULER = IP_ADDRESSES.find_one({'name': 'Scheduler'})['url']
    return render_template("sensor_location.html", error=error, given_app_id = given_app_id, username = payload['sub'], SCHEDULER = SCHEDULER, URL = SENSOR_BINDER,sensor_kinds=sensor_kinds, sensor_count=sensor_count)

@app.route('/register/<user_type>', methods = ['POST'])
def register(user_type):
    username=request.form['username']
    password=request.form['password']
    if not is_local:
        AUTHENTICATION_MANAGER = IP_ADDRESSES.find_one({'name': 'Authentication_Manager'})['url']
    CREATE_URL = AUTHENTICATION_MANAGER + '/create_user/'
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
    AUTHENTICATION_MANAGER = 'http://127.0.0.1:5001'
    if not is_local:
        AUTHENTICATION_MANAGER = IP_ADDRESSES.find_one({'name': 'Authentication_Manager'})['url']
    AUTH_URL = AUTHENTICATION_MANAGER + '/authenticate_user/'
    response = requests.post(AUTH_URL+user_type,json={'username':username,'password':password}).content.decode()
    payload = json.loads(response)
    if(payload["message"]=="Success"):
        return dashboard(user_type, payload['auth_token']);    
    else:
        return render_template('signin_page.html', user_type =  user_type, authcode="error_login", mesg = payload["message"])

@app.route('/Schedule/',methods= ['GET','POST'])
def schedule():
    SCHEDULER = "http://127.0.0.1:5011"
    auth_token=""
    if auth_token == "":
        auth_token = request.headers.get('Authorization')
        if auth_token == None:
            auth_token = request.cookies.get('auth_token')
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
    except:
        return session_expired("End_User",'')   
    if not is_local:
        SCHEDULER = IP_ADDRESSES.find_one({'name': 'Scheduler'})['url']
    return render_template("temp.html",username=payload['sub'],user_type="End_User",token=auth_token,URL=SCHEDULER)


@app.route('/Success/',methods= ['GET','POST'])
def success():
    REQUEST_MANAGER = 'http://127.0.0.1:5000'
    if not is_local:
        REQUEST_MANAGER =  IP_ADDRESSES.find_one({'name': 'Request_Manager'})['url']
    return render_template("success.html",URL=REQUEST_MANAGER)

@app.route('/Upload/<user_type>', methods = ['POST'])
def upload(user_type):
    auth_token = request.cookies.get('auth_token')
    DEPLOYER = "http://127.0.0.1:5005"
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
        if not is_local:
            DEPLOYER = IP_ADDRESSES.find_one({'name': 'Deployment_Manager'})['url']
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
            return dashboard(user_type,auth_token)
            #return render_template("temp.html",username=username,user_type=user_type,token=auth_token,URL=SCHBACK)
        else:
            return response
    except Exception as e:
        return session_expired(user_type,str(e))

@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"

if(__name__ == '__main__'):
    app.run(host ='0.0.0.0',port=5000,debug=True)