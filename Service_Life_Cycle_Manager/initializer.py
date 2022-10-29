import paramiko
import json
import os
import time
import vm_provisioner
from flask import Flask , request, redirect
from pymongo import MongoClient
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient
from pymongo import MongoClient
from threading import Thread

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secretkey'
CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
# CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
# client = MongoClient(CONNECTION_STRING)
# dbname = client['nodeManager']
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"
CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"
ip_dbname = client['AI_PLATFORM']
IP_ADDRESSES = ip_dbname["MODULE_URL"]

#app = dbname["VM_DETAILS"]
is_local = False
REQUEST_MANAGER = 'http://127.0.0.1:5000'
f = open('./subscription_config.json')
subs = json.load(f)
subscription_id = subs["id"]
credentials = subs["credentials"]

f1 = open('./vm_user_config.json')
vm_user = json.load(f1)
# f2 = open('./vm_details.json')
# vm_details = json.load(f2)
vm_details_db = ip_dbname["VM_DETAILS"]
vm_details_collection = vm_details_db.find({})
vm_details = {}
for x in vm_details_collection:
    vm_details[x['name']]=x
f3 = open('./initializer_config.json')
initialize_details = json.load(f3)

def zookeper_initializer(vm_ip, username , password):
    print("Starting Kafka..")
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(vm_ip, 22, username , password)
    command="sudo ~/Kafka/bin/zookeeper-server-start.sh ~/Kafka/config/zookeeper.properties"
    stdin,stdout,stderr =s.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()   
    print(lines)

def kafka_server_initializer(vm_ip, username , password):
    time.sleep(10)
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(vm_ip, 22, username , password)
    command="sudo JMX_PORT=8004 ~/Kafka/bin/kafka-server-start.sh ~/Kafka/config/server.properties"
    stdin,stdout,stderr =s.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()   
    print(lines)
    print("Kafka Probably Started...")

def kafka_initializer(s,service_name,vm_ip,username , password,source,destination,source_path,folder_name):
    command="pip install grpcio"
    stdin,stdout,stderr =s.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()   
    print(lines)
    print("Initializing Kafka..", flush=True)
    r = upload_container(s,service_name,vm_ip,source,destination,source_path,folder_name)
    sftp_client = s.open_sftp()
    if r == 0:
        print("Initializing Kafka..")
        sftp_client.put('./kafka_initializer.py' , './kafka_initializer.py')
        command="python3 kafka_initializer.py http://'"+vm_ip+"'"
        stdin,stdout,stderr =s.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()   
        print(lines)
        time.sleep(1)
        command="sudo chmod +x Kafka/bin/*.sh"
        stdin,stdout,stderr =s.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()   
        print(lines)
        command="sudo apt install -y default-jre"
        stdin,stdout,stderr =s.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()   
        print(lines)
    

    zookeper_thread = Thread(target = zookeper_initializer, args = [vm_ip,username , password])
    zookeper_thread.start()

    kafka_server_thread = Thread(target = kafka_server_initializer, args = [vm_ip,username , password])
    kafka_server_thread.start()

    zookeper_thread.join()
    kafka_server_thread.join()

def initialize_env(s,vm_ip):
    print("++++Initializing Environment")

    build_cmd = "sudo apt-get update"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)

    build_cmd = "pip3"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)

    if len(lines)<=10:
        print("pip3 not found!")
        build_cmd = "sudo apt install -y python3-pip"
        stdin,stdout,stderr = s.exec_command(build_cmd)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
        print(lines)

    
        print("pip3 installed")

    build_cmd = "pip3 install azure-storage-file-share"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)

    build_cmd = "pip"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)

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
    #print(lines)
    # build_cmd = "pip install azure-storage-file-share"
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
    exit_status = stdout.channel.recv_exit_status()
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
        sftp_client.put('./download_code_base.py' , './download_code_base.py')
        time.sleep(1)
        print("++++ Downloading Strating..... ")
        command="python3 download_code_base.py '"+source_path+"' '"+ folder_name +"'"
        stdin,stdout,stderr =s.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()   
        print(lines)
        time.sleep(1)
        return 0
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
        return 1
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
    #print(lines)

    buil_cmd = "sudo systemctl enable docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)
    time.sleep(1)
    buil_cmd = "sudo systemctl status docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    exit_status = stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    #print(lines)

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


def restart_vm(VM_IP):
    for i in vm_details.keys():
        if vm_details[i]['ip'] == VM_IP :
            VM_NAME = i
            GROUP_NAME = vm_details[i]['group']
            compute_client = ComputeManagementClient(credentials, subscription_id)
            async_vm_restart = compute_client.virtual_machines.restart(
                    GROUP_NAME, VM_NAME)
            async_vm_restart.wait()
            break

# for key in initialize_details:
# initialize_docker_env("VM2")
# upload_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
# initialize_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
# start_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
#upload_container("Request_Manager",5000, "VM2","./Request_Manager/","~/Request_Manager/")
#initialize_containers("Request_Manager",5000, "VM1","./Request_Manager/","~/Request_Manager/")

@app.route('/Initialize_Environment',methods = ['POST'])
def init():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    username = vm_details[initialize_details['service_name']["vm_name"]]["username"]
    password = vm_details[initialize_details['service_name']["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)

    vm_ip = request.get_json()['vm_ip']
    initialize_docker_env(s,vm_ip)

@app.route('/Upload',methods = ['POST'])
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

@app.route('/Containerize',methods = ['POST'])
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

@app.route('/Deploy',methods = ['POST'])
def deploy():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    
    service_name = request.get_json()['name']
    URL = request.get_json()['url']
    start = URL.rfind("/")+1
    end = URL.rfind(":")
    vm_ip = URL[start:end]
    port = URL[end+1:]

    username = vm_details[initialize_details[service_name]["vm_name"]]["username"]
    password = vm_details[initialize_details[service_name]["vm_name"]]["password"]
    s.connect(vm_ip, 22, username , password)
    
    start_container(s,service_name,vm_ip,port)
    return "ok"

@app.route('/restart',methods = ['POST'])
def restart():
    
    server_ip = request.get_json()['Server_ip']
    restart_vm(server_ip)
    app.update_one({"ip":server_ip},{"$set":{"status": "active"}})

@app.route('/provision',methods = ['POST'])
def provision():
    vm_name = request.form['vm_name']
    username = request.form['username']
    password = request.form['password']
    vm_ip = vm_provisioner.provision_vm(vm_name, username, password)
    
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(vm_ip, 22, username , password)
    time.sleep(10)
    initialize_env(s,vm_ip)
    initialize_docker_env(s,vm_ip)

    REQUEST_MANAGER = ""
    if is_local == False:
        REQUEST_MANAGER = IP_ADDRESSES.find_one({'name':'Request_Manager'})['url']
    redir = redirect(REQUEST_MANAGER + "/Success")
    return redir
    #app.update_one({"ip":server_ip},{"$set":{"status": "active"}})

@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"

# def sperate_out_vms(vms):
#     list_of_list = []
#     list_of_keys = []
#     last_key = ""
#     for key in vms:
#         print(key[0])
#         if last_key != key[0]:
#             list_of_keys = []
#             last_key = key[0]
#         else:
#             list_of_list.append(list_of_keys)
#         list_of_keys.append(key[0])
    
#     return list_of_list
    
def sperate_out_vms(initialize_details):
    dict_of_list = {}
    last_key = ""
    for key in initialize_details:
        if initialize_details[key]["vm_name"] not in dict_of_list :
            dict_of_list[initialize_details[key]["vm_name"]] = []
        dict_of_list[initialize_details[key]["vm_name"]].append(key)
    return dict_of_list

def deploy_on_vm(dict_of_lists, key):
    s = paramiko.SSHClient()
    kafka_thrd = None
    flag = False
    
    for key in dict_of_lists[key]:
        print("+++++++++++++++++++++++++++++++++++++++++++")
        print(key)
        print("+++++++++++++++++++++++++++++++++++++++++++")
        vm_ip = vm_details[initialize_details[key]["vm_name"]]["ip"]
        source = initialize_details[key]["source"]
        destination = initialize_details[key]["destination"]
        source_path = initialize_details[key]["source_path"]
        folder_name = initialize_details[key]["folder_name"]
        service_name = key
        path = destination
        port = initialize_details[key]["port"]
        username = vm_details[initialize_details[key]["vm_name"]]["username"]
        password = vm_details[initialize_details[key]["vm_name"]]["password"]
        if flag == False:
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(vm_ip, 22, username , password)
            flag = True
        initialize_env(s,vm_ip)
        if key != "Kafka":
            initialize_docker_env(s,vm_ip)
            upload_container(s,service_name,vm_ip,source,destination,source_path,folder_name)
            time.sleep(10)
            initialize_container(s,service_name,vm_ip,path,port)
            time.sleep(10)
            start_container(s,service_name,vm_ip,port)
            print(key + " Deployed")
            a = IP_ADDRESSES.find_one({'name':key})
            print(a)
            if a != None:
                if a['url'] != "http://" +vm_ip +":"+ str(port):
                    IP_ADDRESSES.update_one({'name':key},{'$set':{'name':key,'url':"http://" +vm_ip +":"+ str(port)}})
            else:
                IP_ADDRESSES.insert_one({'name':key,'url':"http://" +vm_ip +":"+ str(port)})
    
        else:
            # kafka_thrd = Thread(target = kafka_initializer, args = [s,service_name,vm_ip,username , password,source,destination,source_path,folder_name])
            # kafka_thrd.start()
            pass
        
    if kafka_thrd != None:
        kafka_thrd.join()
        
def flask_app():
    app.run(host ='0.0.0.0',port=8000,debug=False)

if(__name__ == '__main__'):   
    cmd = 'az login --service-principal -u "70d4dd84-669a-442b-bd60-0aac99f75f47" -p "T4C9OhLGk4M.DGX7YUkvegE-B2LP2SyT0l" --tenant "031a3bbc-cf7c-4e2b-96ec-867555540a1c"'
    os.system(cmd)
    #client.connect("20.213.161.182", 22, "IASHackathon1", "IASHackathon1")
    #client.connect("20.216.18.166", 22, username =  "azureuser", password = "@mazingSpiderMan",allow_agent=True,look_for_keys = False)
    
    for key in initialize_details:
        vm_ip = vm_details[initialize_details[key]["vm_name"]]

    # new_list = sorted(initialize_details.items(), key=lambda x: x[1]['vm_name'], reverse=False)
    
    dict_of_lists = sperate_out_vms(initialize_details);
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")

    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print(dict_of_lists)
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    i = 0
    thread_list = [None] * len(dict_of_lists)
    thread_flask =  Thread(target = flask_app)
    thread_flask.start()
    for key in dict_of_lists:
        thread_list[i] = Thread(target = deploy_on_vm, args = [dict_of_lists,key])
        thread_list[i].start()
        i += 1

    for i in thread_list:
        i.join()
    
    thread_flask.join()
    
    