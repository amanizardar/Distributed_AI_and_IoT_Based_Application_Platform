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
# from azure.mgmt.compute import ComputeManagementClient


# from azure.common.credentials import ServicePrincipalCredentials

# from azure.identity import ClientSecretCredential
# from azure.mgmt.compute import ComputeManagementClient




# from azure.identity import ClientSecretCredential
# from azure.mgmt.compute import ComputeManagementClient


from time import sleep

app = Flask(__name__)


#  monitoring_app_and_models() will monitor the applications and models . 
#  monitoring_services() will monitor the modules such as request manager, scheduler etc...
#  monitoring_servers() will monitor the vm's .



# application_table_name="app_nodes"
# Model_table_name="model_nodes"
service_ok_code="ok"
server_ok_code="ok"
connection_string= "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
deployer_MODEL_URL="/ftApp/"
deployer_APP_URL="/ftModel/"
global_database_name="AI_PLATFORM"
table_name_of_apps="app_nodes"   #app user nodes is being used
table_name_of_models="model_nodes"

table_name_of_service="service_nodes"
table_name_of_server="VM_DETAILS"
ip_column_name_apps="ip"
port_column_name_apps="port"
name_column_name_apps="app"
ip_column_name_models="ip"
port_column_name_models="port"
name_column_name_models="model"
ip_column_name_service="ip"
port_column_name_service="port"
name_column_name_service="service_name"
Server_life_cycle_manager_URL=""
status_column_of_server="status"
vm_ip_column="ip"
vm_username="username"
vm_password="password"
Bootstrapper_URL=""
resource_group_name="IAS_PROJECT"

Vm_name_column="name"

# col = dbname["VM_DETAILS"]




SUBSCRIPTION_ID = 'e469496e-1288-4e2c-97c5-77fad883bc8a'
GROUP_NAME = 'IAS_PROJECT'
LOCATION = ''





client = MongoClient(connection_string)
database_name=global_database_name
monitoring_db=client[database_name]


# @app.route("/healthcheck")
# def health():
#     return "ok"





def monitoring_apps():
    print("Monitoring of apps Started...")

    while(1):
        collection_name=table_name_of_apps
        app1=monitoring_db[collection_name]

        # documents=[{"ied":1,"ip":"159.90.87.76","port":5000},{"ied":2,"ip":"159.90.57.76","port":6000}]
        # app.insert_many(documents)

        # print(monitoring_db.list_collection_names())



        for document in app1.find({},{name_column_name_apps:1, ip_column_name_apps: 1, port_column_name_apps: 1, "_id": 0 }):
            x=str(document[ip_column_name_apps])
            z=document[port_column_name_apps]
            x+=":"+str(document[port_column_name_apps])
            y=document[name_column_name_apps]
            url = f'http://{x}/healthcheck'

            print(url)
            response = requests.get(url)
            if(response==service_ok_code):
                pass
            else:
                print("APP is down! Sending report to Deployer")

                data={name_column_name_apps:y,ip_column_name_apps:x,port_column_name_apps:z}
                url = 'http://localhost'
                response = requests.post(url+'/deployApp', json=data)


def monitoring_models():
    print("Monitoring of Model Started...")

    while(1):
        collection_name=table_name_of_models
        app=monitoring_db[collection_name]

        # documents=[{"ied":1,"ip":"159.90.87.76","port":5000},{"ied":2,"ip":"159.90.57.76","port":6000}]
        # app.insert_many(documents)

        # print(monitoring_db.list_collection_names())



        for document in app.find({},{name_column_name_models:1, ip_column_name_models: 1, port_column_name_models: 1, "_id": 0 }):
            x=str(document[ip_column_name_models])
            z=document[port_column_name_models]
            x+=":"+str(document[port_column_name_models])
            y=document[name_column_name_models]
            url = f'http://{x}/healthcheck'

            print(url)
            response = requests.get(url)
            if(response==service_ok_code):
                pass
            else:
                print("Model is down! Sending report to Deployer")
                data={name_column_name_models:y,ip_column_name_models:x,port_column_name_models:z}
                response = requests.post(deployer_MODEL_URL, json=data)
                url = 'http://localhost'
                response = requests.post(url+'/deployModel', json=data)


        # monitoring of modules (code)
def monitoring_services():
    print("Monitoring of Services Started...")

    while(1):

        collection_name=table_name_of_service
        app1=monitoring_db[collection_name]

        for document in app1.find({},{ ip_column_name_service: 1, port_column_name_service: 1, "_id": 0 }):
            x=str(document[ip_column_name_service])
            z=document[port_column_name_service]
            x+=":"+str(document[port_column_name_service])
            y=document[name_column_name_service]
            url = f'http://{x}/healthcheck'

            response = requests.get(url)
            if(response==server_ok_code):
                pass
            else:
                print("Service is down! Sending report to Bootstrapper")

                data={name_column_name_service:y,ip_column_name_service:x,port_column_name_service:z}
                #url = 'http://localhost'
                #response = requests.post(url+'/deployModel', json=data)


# def monitoring_servers():
#     print("Monitoring of Servers Started...")


    
#     collection_name=table_name_of_server
#     app2=monitoring_db[collection_name]

    
#     credential = ClientSecretCredential(
#     tenant_id='031a3bbc-cf7c-4e2b-96ec-867555540a1c',
#     client_id='c8143046-faf2-48b7-b373-eb12f5040cd5',
#     client_secret='vqP7Q~XOGUQIV9~c2KVwSORVMXNRq11_o~I8A'
#     )

#     compute_client = ComputeManagementClient(
#         credential=credential,
#         subscription_id=SUBSCRIPTION_ID
#     )

#     while(1):


#         for document in app2.find({},{"status":1, Vm_name_column: 1,vm_ip_column:1, "_id": 0 }):
#             if(document["status"]=="active"):
#                 vm = compute_client.virtual_machines.get(GROUP_NAME, document[Vm_name_column], expand='instanceView')
#                 for stat in vm.instance_view.statuses:

#                     if(stat[1].display_status=="VM deallocated" or stat[1].display_status=="VM Stopped"):

#                         # DB Change



#                         app2.update_one({Vm_name_column:document[Vm_name_column]},{"$set":{status_column_of_server:"Inactive"}})

#                         # End Of DB Change


#                         print("VM is down! Sending report to Server life Cycle manager")
#                         # data={Vm_name_column:document[Vm_name_column],vm_ip_column:document[vm_ip_column],vm_username:document[vm_username],vm_password:document[vm_password]}
#                         # response = requests.post(Server_life_cycle_manager_URL, json=data)
#                 sleep(240)



        # for document in app2.find({},{ ip_column_name_service: 1, port_column_name_server: 1, "_id": 0 }):
        #     x=str(document[ip_column_name_service])
        #     z=document[port_column_name_server]
        #     x+=":"+str(document[port_column_name_server])
        #     y=document[id_column_name_server]
        #     url = f'http://{x}/healthcheck'

        #     response = requests.get(url)
        #     if(response==server_ok_code):
        #         pass
        #     else:

        #         data={id_column_name_server:y,ip_column_name_service:x,port_column_name_server:z}
        #         response = requests.post(deployer_URL, json=data)


        # sleep(240)
        
# /////////////////////////////


def monitoring_vm():
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    col = dbname["VM_DETAILS"]
    while True:
        query = {"status":"active"}

        vms = []
        res = col.find(query)
        for x in res:
            vms.append(x['ip'])
        
        print(vms)
        
        for vm in vms:
            hostname = vm 
            response = os.system("ping -t 1 -c 1 " + hostname)
            if response == 0:
                print(hostname, ' is up!')
            else:
                print(hostname, ' is down!')
                ip_dbname = client['AI_PLATFORM']
                IP_ADDRESSES = ip_dbname["MODULE_URL"]
                Service_Life_Cycle_Manager = IP_ADDRESSES.find_one({'name': 'Service_Life_Cycle_Manager'})['url']
                data = {'Server_ip':hostname}
                response = requests.post(Service_Life_Cycle_Manager+"/restart", json=data)
            time.sleep(5)
        time.sleep(5)
# /////////////////////////////


# t1=Thread(target=monitoring_apps)
# t2=Thread(target=monitoring_services)
# t3=Thread(target=monitoring_servers)
t4=Thread(target=monitoring_vm)
# t1.start()
# t2.start()
# t3.start()
t4.start()
# t1.join()
# t2.join()
# t3.join()
t4.join()


    


# client = MongoClient('localhost', 27017)
# db = client.flask_db
# todos = db.todos
# CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
# dbname = client[table_name]
# apps=client[dbname]


# client.list_database_names()

# mongo_tables= {
# "Apps" : dbname[application_table_name],
# "Models" : dbname[Model_table_name]
# }



# for document in mongo_tables["Apps"].find({},{ "id_of_it": 1,"ip": 1, "port": 1, "_id": 0 }):
#     x=str(document['ip'])
#     x+=":"+str(document['port'])
#     url = f'http://{x}/healthcheck'
#     # data = {'arr': int(data_to_send)}

#     response = requests.get(url)
#     if(response==service_ok_code):
#         pass
#     else:
#         data={"id":}

    
   


    # response = requests.get(url)

