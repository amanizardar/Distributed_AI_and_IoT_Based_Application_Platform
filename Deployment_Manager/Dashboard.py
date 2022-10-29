#from distutils.log import debug
from flask import Flask, request, redirect
from flask import render_template
#from matplotlib import container
import paramiko
import time
import json
import os
import requests
from pymongo import MongoClient
import Load_Balancer
from flask import Flask
from flask import request
from numpy import source
from pymongo import MongoClient
import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient


app = Flask(__name__)

def wait(t):
    time.sleep(t)

connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"

file_client = ShareFileClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
file_client2 = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"

def create_directory(dir_name):
    try:
        dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except Exception as ex:
        print("ResourceExistsError:", ex)

def Upload_file_and_create_dir(folder_name,filepath):
    try:
        create_directory(folder_name)
        destination_file_path=folder_name+'/'+os.path.basename(filepath)
        print(destination_file_path)
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

        with open(filepath, "rb") as source_file:
            file_client.upload_file(source_file)

        print("Succesfully Uploaded")
    except Exception as E:
        print("File_NOT_found Error")

def upload_file(folder_name,filepath):
    try:
        destination_file_path=folder_name+'/'+os.path.basename(filepath)
        print(destination_file_path)
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

        with open(filepath, "rb") as source_file:
            file_client.upload_file(source_file)

        print("Succesfully Uploaded")
    except Exception as E:
        print("File_NOT_found Error")

def download_azure_file(dir_name, file_name):
    try:
        source_file_path = dir_name + "/" + file_name
        dest_file_name = file_name
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)
        with open(dest_file_name, "wb") as data:
            stream = file_client.download_file()
            data.write(stream.readall())

    except Exception as ex:
        print("ResourceNotFoundError:", ex)

def download_files(folder_name):
    my_directory_client = file_client2.get_directory_client(directory_path=folder_name)
    my_list = list(my_directory_client.list_directories_and_files())
    for file in my_directory_client.list_directories_and_files():
        download_azure_file(folder_name,file["name"])

# download_files('model1_model')

data = {}
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('dashboard.html', authcode=None)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    print("Inside submit ===", flush=True)
    if (request.method == 'POST'):
        f1 = request.files["f1"]
        f2 = request.files["f2"]
        f3 = request.files["f3"]
        data['f1'] = f1.filename
        data['f2'] = f2.filename
        data['f3'] = f3.filename
        f4 = request.files["f4"]
        f5 = request.files["f5"]
        f6 = request.files["f6"]
        data['f4'] = f4.filename
        data['f5'] = f5.filename
        data['f6'] = f6.filename

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname["model_nodes"]
    col2 = dbname["app_nodes"]
    print("line 121 ===")

    if f1.filename!='':
        if f2.filename=='' or f3.filename=='':
            return "All files not uploaded"
    if f2.filename!='':
        if f1.filename=='' or f3.filename=='':
            return "All files not uploaded"
    if f3.filename!='':
        if f1.filename=='' or f2.filename=='':
            return "All files not uploaded"
    if f4.filename!='':
        if f6.filename=='':
            return "All files not uploaded"
    if f6.filename!='':
        if f4.filename=='':
            return "All files not uploaded"
    if f1.filename=='' and f2.filename=='' and f3.filename=='' and f4.filename=='' and f5.filename=='' and f6.filename=='':
        return "No files uploaded"

    if f1.filename!='' and f1.filename[-4:]!=".pkl":
        return "Wrong type of file uploaded - pkl"
    if f2.filename!='' and f2.filename[-3:]!=".py":
        return "Wrong type of file uploaded - py"
    if f3.filename!='' and f3.filename[-5:]!=".json":
        return "Wrong type of file uploaded - json - model"
    if f4.filename!='' and f4.filename[-4:]!=".zip":
        return "Wrong type of file uploaded - zip"
    if f6.filename!='' and f6.filename[-5:]!=".json":
        return "Wrong type of file uploaded - json"

    print("line 152 ===", flush=True)

    if(f1.filename!=''):
        fname_len = len(f1.filename)
        modelName = f1.filename[0:fname_len-4]
        query = {"model":modelName}
        if(len(list(col1.find(query)))>0):
            return "Model already deployed"

    print("line 161 ===", flush=True)

    # if(f4.filename!=''):    
    #     fname_len = len(f4.filename)
    #     appName = f4.filename[0:fname_len-4]
    #     query = {"app":appName}
    #     if(len(list(col2.find(query)))>0):
    #         return "App already deployed"

        
    # print(request.form.get('role'), flush=True)
    # print(request.form.get('username'), flush=True)

    print(data)
    # r = requests.post('http://127.0.0.1:5000/',json=data)

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']
    col1 = dbname["VM_DETAILS"]
    col2 = dbname['model_nodes']

    # username, password, ip = Load_Balancer.choose_best_node()
    # print(ip)

    # myquery = { "ip": ip }
    # vm = col1.find(myquery)
    # service_port = 0
    # for i in vm:
    #     service_port = i["first_free_port"]
    # p = service_port + 1
    # col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})

    role = upload()
    if role == "model":
        print("line 196 ===", flush=True)
        deploy_model(modelName)
    
    return "ok"

@app.route("/deployApp", methods=['GET', 'POST'])
def deployApp():
    print("request recieved in deployApp")
    name = request.json['app_id']#considering name of app is given by deployer in json
    user_name = request.json['username']
    print(request.json)
    download_files(name+"_app")

    wait(2)

    zipfile = name

    username, password, ip = Load_Balancer.choose_best_node()
    print(ip, flush = True)

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, password) 

    stdin,stdout,stderr = s.exec_command('mkdir ./App;ls')
    print(1,stderr.readline(),stdout.readline())

    stdin,stdout,stderr = s.exec_command('sudo apt install unzip')
    print(22,stderr.readline(),stdout.readline())

    ftp_client=s.open_sftp()
    
    ftp_client.put('./'+name+'.zip' , './App/'+zipfile+'.zip')
    time.sleep(0.5)
    print("unzipping")
    stdin,stdout,stderr = s.exec_command('cd App;unzip -o '+zipfile+'.zip')
    print(333,stderr.readline(),stdout.readline())
    print('./App/'+zipfile+'/Dockerfile')
    ftp_client.put('./Dockerfile' , './App/'+zipfile+'/Dockerfile')
    time.sleep(0.5)

    stdin,stdout,stderr = s.exec_command('sudo docker build -t '+zipfile+'_'+user_name+' ./App/'+zipfile+'/')
    print(4444,stderr.readline(),stdout.readline())
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname["VM_DETAILS"]
    myquery = { "ip": ip }
    vm = col1.find(myquery)
    service_port = 0
    for i in vm:
        service_port = i["first_free_port"]
    p = service_port + 1
    col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})

    stdin,stdout,stderr = s.exec_command('sudo docker run -p '+str(service_port)+':5000 '+zipfile+'_'+user_name)
    print(55555,stderr.readline(),stdout.readline())

    # getting image id
    stdin,stdout,stderr = s.exec_command("sudo docker images | head -2 | tail -1 | awk '{print $3}'")
    image_id = str((stdout.readline()))
    image_id = image_id[:-1]
    

    stdin,stdout,stderr = s.exec_command("sudo docker ps -a | head -2 | tail -1 | awk '{print $1}'")
    container_id = str((stdout.readline()))
    container_id = container_id[:-1]
    # todo - put image id in db

    # removing uploaded files and folder
    stdin,stdout,stderr = s.exec_command("cd App;rm "+zipfile+".zip; rm -r "+name)

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    col = dbname["app_user_node"]
    fname_len = len(zipfile + ".zip")
    appName = zipfile
    myquery = {"app":appName,"enduser":user_name}
    col.delete_one(myquery)
    data_entry = [{"app":appName,"enduser":user_name,"ip": ip,"username": username,"password":password,"port":service_port,"image_id":image_id,"container_id":container_id}]

    for i in data_entry:
        a = col.insert_one(i)
    return "ok"

@app.route("/deployModel", methods=['GET', 'POST'])
def ftModel():
    name = request.json['name']#considering name of model is given by deployer in json
    deploy_model(name)
    return "ok"

def upload():
    uploaded_file1 = request.files['f1']
    uploaded_file2 = request.files['f2']
    uploaded_file3 = request.files['f3']
    uploaded_file4 = request.files['f4']
    uploaded_file5 = request.files['f5']
    uploaded_file6 = request.files['f6']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)
    if uploaded_file2.filename != '':
        uploaded_file2.save(uploaded_file2.filename)
    if uploaded_file3.filename != '':
        uploaded_file3.save(uploaded_file3.filename)
    if uploaded_file4.filename != '':
        uploaded_file4.save(uploaded_file4.filename)
    if uploaded_file5.filename != '':
        uploaded_file5.save(uploaded_file5.filename)
    if uploaded_file6.filename != '':
        uploaded_file6.save(uploaded_file6.filename)

    if uploaded_file1.filename != '':
        print("calling script")
        model_name  = uploaded_file4.filename[:-4]
        os.system("python3 DockerFileGenerator.py " + uploaded_file3.filename + " " +  uploaded_file1.filename + " " + model_name)
        os.system("python3 WrapperClassGenerator.py " + uploaded_file2.filename + " " + uploaded_file1.filename)
        print("calling script")
        # os.system(cmd)

        app_or_model_name  = uploaded_file1.filename[:-4]+"_model"

        Upload_file_and_create_dir(app_or_model_name,uploaded_file1.filename)
        upload_file(app_or_model_name,"WrapperClass.py")
        upload_file(app_or_model_name,"Dockerfile")

        return "model"

    else:
        app_or_model_name  = uploaded_file4.filename[:-4]+"_app"

        configFile = open(uploaded_file6.filename,'r')
        config = json.load(configFile)
        configFile.close()
        print("config")
        print(config)
        sensor_data = json.dumps(config["Application"]["sensor"])
        os.system("python3 Application_docker_generator.py " + uploaded_file6.filename + " " + uploaded_file4.filename[:-4]) 

        app_or_model_name  = uploaded_file4.filename[:-4]+"_app"

        CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING)

        dbname = client['AI_PLATFORM']
        app_req_db = dbname["app_requirement"]

        app_req_db.insert_one({"app_id": uploaded_file4.filename[:-4], "app_name": uploaded_file4.filename[:-4], "sensors": sensor_data})

        Upload_file_and_create_dir(app_or_model_name,uploaded_file4.filename)
        upload_file(app_or_model_name,"Dockerfile")      

        return "application"

def deploy_model(name):
    print("In deploy_model 1", flush=True)
    download_files(name+"_model")

    print("after download files", flush=True)

    username, password, ip = Load_Balancer.choose_best_node()

    print("After load balancer ", flush=True)
    print("Chosen load balancer - ")
    print("user - ", username)
    print("password - ", password)
    print("ip - ", ip)

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, password)

    print("after load balancer ", flush=True)

    modelName = name # without .pkl
    stdin,stdout,stderr = s.exec_command('mkdir -p ./Model')
    stdin,stdout,stderr = s.exec_command('cd Model;mkdir ./'+modelName)

    print("after making model folder.", flush=True)

    ftp_client=s.open_sftp()

    ftp_client.put('./Dockerfile' , './Model/'+modelName+'/Dockerfile')
    time.sleep(0.5)
    ftp_client.put('./WrapperClass.py' , './Model/'+modelName+'/WrapperClass.py')
    time.sleep(0.5)
    ftp_client.put('./'+modelName+'.pkl' , './Model/'+modelName+'/'+modelName+'.pkl')
    time.sleep(0.5)

    print("Moved Dockerfile, WrapperClass and pickle file into VM.", flush=True)

    # stdin,stdout,stderr = s.exec_command('cd App')

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname["VM_DETAILS"]
    myquery = { "ip": ip }
    vm = col1.find(myquery)
    service_port = 0
    for i in vm:
        service_port = i["first_free_port"]
    #print(port)
    print("retrived from DB",flush=True)

    # getting frst availab;e port on that VM
    p = service_port + 1
    col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})

    print("Updated DB",flush=True)

    col2 = dbname["model_nodes"]
    myquery = {"model":modelName}
    col2.delete_one(myquery)
    data_entry = [{"ip": ip,"username": username,"password":password,"model":modelName,"port":service_port}]
    for i in data_entry:
        a = col2.insert_one(i)

    print("Building Docker Image",flush=True)
    # Docker Docker
    stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker build . -t '+ modelName)
    print("Model docker image built.",flush=True)
    # App/serviceName/app.py
    print(stderr.readline(),stdout.readline())

    print("Running Docker Container",flush=True)
    stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker run -p '+str(service_port)+':5000 '+modelName)
    print(stderr.readline(),stdout.readline())
    print("Model docker container running.",flush=True)

    os.system("rm WrapperClass.py Dockerfile "+name+".pkl")

    return "ok"

@app.route("/removeApp", methods=['GET', 'POST'])
def removeApp():
    print("request recieved in removeApp")
    # return "from returnApp"
    app_name = request.json['app_id']
    user_name = request.json['username']
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']
    col = dbname['app_user_node']

    myquery = {"app": app_name,"enduser":user_name}
    vm = col.find(myquery)

    #data_entry = [{"app":appName,"enduser":user_name,"ip": ip,"username": username,"password":password,"port":service_port,"image_id":image_id}] 

    # get image id from db
    ip = ""
    port = ""
    image_id = ""
    container_id = ""
    for x in vm:
        ip = x['ip'] 
        port = x['port']
        image_id = x['image_id']
        username = x['username']
        password = x['password']
        image_id = x['image_id']
        container_id = x['container_id']

    print("got data from DB", vm)
    
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, password)

    print("connected with VM")
    # sudo docker images -> list of images
    # sudo docker ps -a -> list of containers
    # sudo docker rmi -f <image id> -> delete docker image
    # sudo docker rm -f <container id> -> delete docker container

    # get image id of deployed docker image and put it into db when deploying
    # sudo docker rmi -f <image id> -> delete docker image
    col.delete_one( { "image_id": image_id } )
    print(request.json, image_id)
    print("removed conatiner from VM")
    stdin,stdout,stderr = s.exec_command("sudo docker rm -f "+str(container_id))
    print("removed image from VM")
    stdin,stdout,stderr = s.exec_command("sudo docker rmi -f "+str(image_id))
    print(stdout.readline(),stderr.readline())
    # remove directory   
    return "ok"

@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"

app.run(host="0.0.0.0",port="5005")