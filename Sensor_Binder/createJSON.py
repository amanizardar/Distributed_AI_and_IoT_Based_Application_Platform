#from concurrent.futures import process
#from re import I, template
import certifi
#import ast
from pymongo import MongoClient
from flask import Flask, render_template, request,redirect
from sensor_binder import *
import requests

app = Flask(__name__)

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

REQUEST_MANAGER =  'http://127.0.0.1:5000'
SCHEDULER = "http://127.0.0.1:5011"
dbname = client['AI_PLATFORM']
app_req_db = dbname["app_requirement"]

IP_ADDRESSES = dbname["MODULE_URL"]

is_local = False

# ip_table = list(IP_ADDRESSES.find())
# for i in ip_table:
#     if 'REQUEST_MANAGER' in i:
#         REQUEST_MANAGER = i['REQUEST_MANAGER']
#     if 'SCHEDULER' in i:
#         SCHEDULER = i['SCHEDULER']

@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"

@app.route("/jsonifyRequest", methods=['POST', 'GET'])
def sensor_requirements():
    auth_token = request.cookies.get('auth_token')
    # request_details = {"info" : list()}
    # new_sensor_instance = request.form.to_dict()
    # # print(new_sensor_instance)
    # for each in new_sensor_instance:
    #     l = each.split('_')
    #     # print (l)
    #     val = {"type" : l[0] , "location" : new_sensor_instance[each]}
    #     request_details["info"].append(val)

    # # print(request_details)
    # #SCHEDULER = new_sensor_instance["SCHEDULER"]
    # binding_map = processRequest(request_details)
    # scheduling_data = {"app_id": given_app_id,"info" : binding_map}
    # # print(scheduling_data)s
    # response=requests.post( SCHEDULER+ "/schedule_data",json=scheduling_data).content.decode()
   
    
    # redir = redirect(REQUEST_MANAGER+"/Schedule/")
    # redir.headers['Authorization'] = auth_token
    # return redir
    request_details = {"info" : list()}
    new_sensor_instance = request.form.to_dict()
    # print(new_sensor_instance)
    given_app_id=new_sensor_instance["given_app_id"]
    del new_sensor_instance["given_app_id"]
    sensor_kinds = new_sensor_instance["sensor_kinds"]
    sensor_kinds = sensor_kinds[1:-1].split(",")
    temp = []
    for x in sensor_kinds:
        temp.append(x.strip()[1:-1])
    sensor_kinds = temp
    print(sensor_kinds)

    del new_sensor_instance["sensor_kinds"]

    sensor_count = new_sensor_instance["sensor_count"]
    print(type(sensor_count))
    del new_sensor_instance["sensor_count"]
    sensor_count = sensor_count[1:-1].split(",")
    temp = []
    for x in sensor_count:
        temp.append(int(x.strip()))
    sensor_count = temp
    print("==============++++++++++++++++++++++++++++")
    print(new_sensor_instance)

    for each in new_sensor_instance:
        if each != 'username':
            l = each.split('_')
            print("++++++++++++++++++++++++++++")
            print(l)
            print(l[0])
            print(l[1])
            # i = (l[1].split(' '))[0]
            
            # print (l)
            val = {"type" : l[0] , "location" : new_sensor_instance[each], "serial_num" : l[1]}
            request_details["info"].append(val)

    binding_map = processRequest(request_details)
    print(binding_map)
    if binding_map == None:
        print("Error")
        # redir = redirect(REQUEST_MANAGER+"/sensor_location", code=307)
        # redir.headers['Authorization'] = auth_token
        REQUEST_MANAGER = "http://127.0.0.1:5000"
        if not is_local:
            REQUEST_MANAGER = IP_ADDRESSES.find_one({'name': 'Request_Manager'})['url']
        return redirect(REQUEST_MANAGER+"/sensor_location/", code=307)
        #return render_template("sensor_location.html", error='Sensor not available', given_app_id=given_app_id, sensor_kinds=sensor_kinds, sensor_count=sensor_count)

    else:
        scheduling_data = {"app_id": given_app_id,"info" : binding_map}
        print(scheduling_data)
        REQUEST_MANAGER = "http://127.0.0.1:5000"
        SCHEDULER = "http://127.0.0.1:5011"
        if not is_local:
            SCHEDULER = IP_ADDRESSES.find_one({'name': 'Scheduler'})['url']
        response=requests.post( SCHEDULER+ "/schedule_data",json=scheduling_data).content.decode()
        if not is_local:        
            REQUEST_MANAGER = IP_ADDRESSES.find_one({'name': 'Request_Manager'})['url']
        redir = redirect(REQUEST_MANAGER+"/Schedule/")
        redir.headers['Authorization'] = auth_token
        return redir

# @app.route("/")
# def m():
#     #get_sensors()
#     return render_template("sensor_location.html", sensor_kinds = sensor_kinds, sensor_count=sensor_count)

app.run(port=6005,host="0.0.0.0")