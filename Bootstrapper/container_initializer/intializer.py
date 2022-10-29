import paramiko
import json
import os
import time
from flask import Flask , request
from pymongo import MongoClient
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient

import sys
sys.path.insert(1, './Bootstrapper/vm_provisioning')
import vm_provisioner

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secretkey'

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['nodeManager']
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"

ip_dbname = client['AI_PLATFORM']
IP_ADDRESSES = ip_dbname["MODULE_URL"]

#app1 = dbname["VM_DETAILS"]

f = open('./Bootstrapper/subscription_config.json')
subs = json.load(f)
subscription_id = subs["id"]
credentials = subs["credentials"]

f1 = open('./Bootstrapper/vm_user_config.json')
vm_user = json.load(f1)
# f2 = open('./Bootstrapper/vm_details.json')
# vm_details = json.load(f2)
vm_details_db = ip_dbname["VM_DETAILS"]
vm_details_collection = vm_details_db.find({})
vm_details = {}
for x in vm_details_collection:
    vm_details[x['name']]=x
# print(vm_details["VM1"]["ip"])

f3 = open('./Bootstrapper/container_initializer/bootstrap_initializer_config.json')

f4 = open('./Bootstrapper/container_initializer/initializer_config.json')
slcm_initialize_details = json.load(f3)
initialize_details = json.load(f4)

def initialize_env(s,vm_ip):
    print("++++Initializing Environment")
    build_cmd = "sudo apt-get update"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    build_cmd = "pip3"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    if len(lines)<=10:
        print("pip3 not found!")
        build_cmd = "sudo apt install -y python3-pip"
        stdin,stdout,stderr = s.exec_command(build_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

    
        print("pip3 installed")

    build_cmd = "pip"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    if len(lines)<=10:
        print("pip not found!")
        build_cmd = "sudo apt install -y python-pip"
        stdin,stdout,stderr = s.exec_command(build_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

    
        print("pip installed")

    build_cmd = "pip install azure-storage-file-share"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    # build_cmd = "pip3 install azure-storage-file-share"
    # stdin,stdout,stderr = s.exec_command(build_cmd)
    # exit_status = stdout.channel.recv_exit_status()
    # lines = stdout.readlines()
    # print(lines)

def initialize_docker_env(s,vm_ip):
    print("++++Initializing Docker Environment")
    build_cmd = "docker -v"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    if len(lines)==0:
        build_cmd = "curl -fsSL https://get.docker.com -o get-docker.sh"
        stdin,stdout,stderr = s.exec_command(build_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

        buil_cmd = "sh get-docker.sh"
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

        buil_cmd = "curl -fsSL https://test.docker.com -o test-docker.sh"
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

        buil_cmd = "sh test-docker.sh" 
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)
        
        buil_cmd = "sh install.sh" 
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

        buil_cmd = "docker -v" 
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)
    else:
        print("Docker Environment Present!")


def upload_container(s,service_name,vm_ip,source,destination,source_path,folder_name):
    print("++++Downloading Code : "+ service_name)
    sftp_client = s.open_sftp()

    localfolder = source
    basefolder = destination

    command="ls"
    stdin,stdout,stderr =s.exec_command(command)
    lines = stdout.readlines()   
    print(lines)
    flag = False
    for i in lines:
        print(i[:-1])
        if service_name == i[:-1]:
            flag = True
            break;
    
    if flag == False:
        print("\t++++ Sending Script...")
        sftp_client.put('./Bootstrapper/container_initializer/download_code_base.py' , './download_code_base.py')
        time.sleep(1)
        print("++++ Downloading Strating..... ")
        command="python3 download_code_base.py '"+source_path+"' '"+ folder_name +"'"
        stdin,stdout,stderr =s.exec_command(command)
        lines = stdout.readlines()   
        print(lines)
        time.sleep(1)
        # command="sudo rm download_code_base.py"
        # stdin,stdout,stderr =s.exec_command(command)
        # lines = stdout.readlines()   
        # print(lines)
        
        # for path,dirs,files in os.walk(localfolder):
        #     if path.lstrip(localfolder)!=None:       
        #         extrapath=path.split(basefolder)[-1]   
        #         command="cd root"  
        #         stdin,stdout,stderr = client.exec_command(command)
        #         command="mkdir {}".format(extrapath)
        #         client.exec_command(command)
        #         lines = stdout.readlines()   
        #         print(lines)
                
        #     for file in files:  
        #         filepath=os.path.join(path,file)
        #         extrapath=path.split(basefolder)[-1]
        #         command="cd root"  
        #         stdin,stdout,stderr = client.exec_command(command)
        #         sftp_client.put(filepath,"{}/{}".format(extrapath,file))
    else:
        print(service_name+" Dir already Present")

    sftp_client.close()

def initialize_container(s,service_name,vm_ip,path,port):
    
    buil_cmd = "[[docker images -q {"+service_name.lower()+"}]]|| echo 1"
    #buil_cmd = "[[docker ps -q -f name={"+service_name.lower()+"}]] || echo 1"
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    # if lines[0]!='1\n':
    print("++++Starting Docker Environemnt........  ")
    buil_cmd = "sudo systemctl start docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sudo systemctl enable docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)
    time.sleep(1)
    buil_cmd = "sudo systemctl status docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sudo docker info" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)
    
    print("++++Checking if images already exists !.......")
    buil_cmd = "sudo docker images -q "+service_name.lower()
    #buil_cmd = "[[docker images -q {"+service_name.lower()+"}]]|| echo 1"
    #buil_cmd = "[[docker ps -q -f name={"+service_name.lower()+"}]] || echo 1"
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)

    if len(lines)==0 :
        print("++++Making Docker imgaes........  "+ service_name.lower())
        buil_cmd = "sudo docker build -t "+ service_name.lower() + " " + path
        stdin,stdout,stderr = s.exec_command(buil_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)
        IP_ADDRESSES.insert_one({'name':key,'url':"http://" +vm_ip +":"+ str(port)})
    else:
        print("Image already present")
    

def start_container(s,service_name,vm_ip,port):
    #buil_cmd = "[[docker ps -q -f name={"+service_name.lower()+"}]] || echo 1"
    print("++++Checking if Docker cotainer........  "+ service_name.lower()+" already running....")
    buil_cmd = "sudo docker ps -q --filter ancestor="+service_name.lower()
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    print(lines)
    

    if len(lines)==0 :
        print("++++Starting Docker imgaes........  "+ service_name.lower())
        run_cmd = "sudo docker run -p "+ str(port)+":"+str(port)+" "+ service_name.lower()
        s.exec_command(run_cmd)
        exit_status = stdout.channel.recv_exit_status()
        print("Started Container....")
    else:
        print("VM already Up and running")


# def restart_vm(GROUP_NAME,VM_IP):
#     for i in vm_details.keys():
#         if vm_details[i]['ip'] == VM_IP :
#             VM_NAME = i
#             GROUP_NAME = vm_details[i]['group']
#             compute_client = ComputeManagementClient(credentials, subscription_id)
#             async_vm_restart = compute_client.virtual_machines.restart(
#                     GROUP_NAME, VM_NAME)
#             async_vm_restart.wait()
#             break


# for key in initialize_details:
# initialize_docker_env("VM2")
# upload_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
# initialize_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
# start_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
#upload_container("Request_Manager",5000, "VM2","./Request_Manager/","~/Request_Manager/")
#initialize_containers("Request_Manager",5000, "VM1","./Request_Manager/","~/Request_Manager/")

#@app.route('/Initialize_Environment',methods = ['POST'])
def init():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    username = vm_details[initialize_details['service_name']["vm_name"]]["username"]
    password = vm_details[initialize_details['service_name']["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)

    vm_ip = request.get_json()['vm_ip']
    initialize_docker_env(s,vm_ip)

#@app.route('/Upload',methods = ['POST'])
def upload():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    username = vm_details[initialize_details['service_name']["vm_name"]]["username"]
    password = vm_details[initialize_details['service_name']["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)

    vm_ip = request.get_json()['vm_ip']
    source = request.get_json()['source']
    destination = request.get_json()['destination']
    upload_container(s,vm_ip,source,destination)

#@app.route('/Containerize',methods = ['POST'])
def containerize():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    username = vm_details[initialize_details['service_name']["vm_name"]]["username"]
    password = vm_details[initialize_details['service_name']["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)

    service_name = request.get_json()['service_name']
    vm_ip = request.get_json()['vm_ip']
    path = request.get_json()['path']
    initialize_container(s,service_name,vm_ip,path)

#@app.route('/Deploy',methods = ['POST'])
def deploy():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    username = vm_details[initialize_details['service_name']["vm_name"]]["username"]
    password = vm_details[initialize_details['service_name']["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)
    
    service_name = request.get_json()['service_name']
    vm_ip = request.get_json()['vm_ip']
    port = request.get_json()['port']
    start_container(s,service_name,vm_ip,port)

#@app.route('/restart',methods = ['POST'])
def restart():
    service_ip = request.get_json()['Server_ip']
    username = request.get_json()['username']
    password = request.get_json()['password']
    #restart_vm(service_ip,vm_ip,port)
    #app1.updtae_one({"ip":service_ip},{"$set":{"status": "active"}})


if(__name__ == '__main__'):  
    
    
    #client.connect("20.213.161.182", 22, "IASHackathon1", "IASHackathon1")
    #client.connect("20.216.18.166", 22, username =  "azureuser", password = "@mazingSpiderMan",allow_agent=True,look_for_keys = False)
    vm_provisioner.provision_vm()
    time.sleep(5)
    print(vm_details)
    vm_details_collection = vm_details_db.find({})
    vm_details = {}
    for x in vm_details_collection:
        vm_details[x['name']]=x
    INIT_DETAILS = ip_dbname["INIT_DETAILS"]
    for key in initialize_details:
        a = INIT_DETAILS.find_one({'name':key})
        if a != None:
            if a['vm_name'] != initialize_details[key]['vm_name']:
                INIT_DETAILS.update_one({'name':key},{'$set':{'vm_name':initialize_details[key]['vm_name']}})
        else:
            dict = initialize_details[key]
            dict['name']=key
            INIT_DETAILS.insert_one(dict)
        

    for key in slcm_initialize_details:
        vm_ip = vm_details[slcm_initialize_details[key]["vm_name"]]["ip"]
        source = slcm_initialize_details[key]["source"]
        destination = slcm_initialize_details[key]["destination"]
        source_path = slcm_initialize_details[key]["source_path"]
        folder_name = slcm_initialize_details[key]["folder_name"]
        service_name = key
        path = destination
        port = slcm_initialize_details[key]["port"]
        username = vm_details[slcm_initialize_details[key]["vm_name"]]["username"]
        password = vm_details[slcm_initialize_details[key]["vm_name"]]["password"]
        
        a = IP_ADDRESSES.find_one({'name':key})
        if a != None:
            if a['url'] != "http://" +vm_ip +":"+ str(port):
                IP_ADDRESSES.update_one({'name':key},{'$set':{'name':key,'url':"http://" +vm_ip +":"+ str(port)}})
        else:
            IP_ADDRESSES.insert_one({'name':key,'url':"http://" +vm_ip +":"+ str(port)})

        if slcm_initialize_details[key]["vm_name"] != "VM0":
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(vm_ip, 22, username , password)

            initialize_env(s,vm_ip)
            initialize_docker_env(s,vm_ip)
            upload_container(s,service_name,vm_ip,source,destination,source_path,folder_name)
            time.sleep(10)
            initialize_container(s,service_name,vm_ip,path,port)
            time.sleep(10)
            start_container(s,service_name,vm_ip,port)
            print(key + " Deployed")
    
    exit()
        
            
    #app.run(host ='0.0.0.0',port=8000,debug=True)