from pydoc import doc
from flask import Flask, request, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import requests
# import datetime
# import jwt
from pymongo import MongoClient
from threading import Thread
import time

import os


from time import sleep

app = Flask(__name__)


service_ok_code="ok"
server_ok_code="ok"
connection_string= "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
deployer_MODEL_URL="/ftApp/"
deployer_APP_URL="/ftModel/"
# global_database_name="AI_PLATFORM"
table_name_of_apps="app_nodes"   #app user nodes is being used
table_name_of_models="model_nodes"

# col = dbname["VM_DETAILS"]

SUBSCRIPTION_ID = 'e469496e-1288-4e2c-97c5-77fad883bc8a'
GROUP_NAME = 'IAS_PROJECT'
LOCATION = ''


client = MongoClient(connection_string)
monitoring_db=client['AI_PLATFORM']


# @app.route("/healthcheck")
# def health():
#     return "ok"

def monitoring_apps():
    print("Monitoring of apps Started...")

    while(1):

        app1=monitoring_db["app_user_node"]

        # documents=[{"ied":1,"ip":"159.90.87.76","port":5000},{"ied":2,"ip":"159.90.57.76","port":6000}]
        # app.insert_many(documents)
        # print(monitoring_db.list_collection_names())

        for document in app1.find({}):
            x=str(document["ip"])
            z=document["port"]
            x+=":"+str(z)
            y=document["app"]
            url = f'http://{x}/healthCheck'

            print(url)
            response = requests.get(url)
            if(response == service_ok_code):
                pass
            else:
                print("APP is down! Sending report to Deployer")
                u=document["enduser"]
                data = {"app_id":y,"ip":x,"port":z,'username':u}
                ip_dbname = client['AI_PLATFORM']
                IP_ADDRESSES = ip_dbname["MODULE_URL"]
                Deployment_Manager = IP_ADDRESSES.find_one({'name': 'Deployment_Manager'})['url']
                response = requests.post(Deployment_Manager+'/deployApp', json=data)


def monitoring_models():
    print("Monitoring of Model Started...")

    while(1):
        app=monitoring_db["model_nodes"]

        for document in app.find({}):
            x=str(document["ip"])
            z=document["port"]
            x+=":"+str(document["port"])
            y=document["model"]
            url = f'http://{x}/healthCheck'

            print(url)
            response = requests.get(url)
            if(response==service_ok_code):
                pass
            else:
                print("Model is down! Sending report to Deployer")
                data={"name":y,"ip":x,"port":z}
                response = requests.post(deployer_MODEL_URL, json=data)
                ip_dbname = client['AI_PLATFORM']
                IP_ADDRESSES = ip_dbname["MODULE_URL"]
                Deployment_Manager = IP_ADDRESSES.find_one({'name': 'Deployment_Manager'})['url']
                response = requests.post(Deployment_Manager+'/deployModel', json=data)
        # monitoring of modules (code)

def monitoring_services():
    print("Monitoring of Services Started...")

    app1=monitoring_db["MODULE_URL"]
    
    
    while(True):
        print("+")
        all_services = app1.find({})
        print(all_services)
        for document in all_services:
            x=document["url"]
            name=document["name"]
            url = f'{x}/healthCheck'
            try:
                response = requests.get(url).content.decode()
                if(response==server_ok_code):
                    print(name + ":" + x +" Service is Up and Running!")
                else:
                    if(name == "Service_Life_Cycle_Manager"):
                        pass
                    else :
                        print(name + ":" + x +" Service is down! Sending report to Bootstrapper")
                        data={"name":name,"url":x}
                        ip_dbname = client['AI_PLATFORM']
                        IP_ADDRESSES = ip_dbname["MODULE_URL"]
                        Service_Life_Cycle_Manager = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
                        response = requests.post(Service_Life_Cycle_Manager+"/Deploy", json=data)
                        time.sleep(15)
            except:
                print(name + ":" + x +" Service is down! Sending report to Bootstrapper")
                data={"name":name,"url":x}
                ip_dbname = client['AI_PLATFORM']
                IP_ADDRESSES = ip_dbname["MODULE_URL"]
                Service_Life_Cycle_Manager = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
                response = requests.post(Service_Life_Cycle_Manager+"/Deploy", json=data)
                time.sleep(15)
            time.sleep(1)

def monitoring_deployment_vm():
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    col = dbname["VM_DETAILS"]
    while True:
        query = {"status":"active"}

        vms = set()
        res = col.find(query)
        for x in res:
            end = x['url'].rfind(":")
            vms.add(x['url'][:end]) 
        print(vms)
        for vm in vms:
            hostname = vm 
            start = hostname.find("/")+2
            response = os.system("ping -t 1 -c 1 " + hostname[start:])
            if response != 0:
                print(vm," Found stopped!!")
                ip_dbname = client['AI_PLATFORM']
                IP_ADDRESSES = ip_dbname["MODULE_URL"]
                Service_Life_Cycle_Manager = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
                data = {'Server_ip':hostname}
                response = requests.post(Service_Life_Cycle_Manager+"/restart", json=data)
            time.sleep(1)
# /////////////////////////////

# def monitoring_service_vm():
#     CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

#     client = MongoClient(CONNECTION_STRING)
#     dbname = client['AI_PLATFORM']
#     col = dbname["MODULE_URL"]
    
#     while True:
    
#         vms = set()
#         res = col.find({})
#         for x in res:
#             end = x['url'].rfind(":")
#             vms.add(x['url'][:end]) 
#         print(vms)
        
#         for vm in vms:
#             hostname = vm 
#             start = hostname.find("/")+2
#             response = os.system("ping -t 1 -c 1 " + hostname[start:])
#             if response != 0:
#                 print(vm," Found stopped!!")
#                 ip_dbname = client['AI_PLATFORM']
#                 IP_ADDRESSES = ip_dbname["MODULE_URL"]
#                 Service_Life_Cycle_Manager = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
#                 data = {'Server_ip':hostname}
#                 response = requests.post(Service_Life_Cycle_Manager+"/restart", json=data)
#                 time.sleep(5)
#             time.sleep(5)
# /////////////////////////////

# t1=Thread(target=monitoring_apps)
# t2=Thread(target=monitoring_models)
# t3=Thread(target=monitoring_servers)
t4=Thread(target=monitoring_services)
# t1.start()
# t2.start()
# # t3.start()
t4.start()
# #t5=Thread(target=monitoring_deployment_vm)
# #t5.start()
# t1.join()
# t2.join()
# # t3.join()
t4.join()
#t5.join()
