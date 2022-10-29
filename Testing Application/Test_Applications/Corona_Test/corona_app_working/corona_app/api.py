#from kafka import KafkaConsumer
import json,requests
from kafka import KafkaConsumer
# from tkinter import N
from pymongo import MongoClient


data = ""

def apiFile(scheduling_data):
    print("In apiFile in api.py")
    global data
    data = scheduling_data["info"]
    print("in api : ",data)

# 
def getSensorData(sensor_type, serial_num, app_id):

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    MODULE_URL_DB = dbname["MODULE_URL"]

    all_instances = dbname["USER_APP_SENSOR"]

    # 
    data_row = list(all_instances.find({"app_id": app_id}))[0]
    
    #
    topic = "" 
    info = data_row["info"]
    for i in info:
        # print(i)
        if(i["type"] == sensor_type and int(i["serial_num"]) == serial_num):
            topic = i["topic"]
            break
            # print(topic)
    
    KAFKA_IP = list(MODULE_URL_DB.find({"name" : "Kafka"}))[0]["url"][7:][:-5]
    print(KAFKA_IP)
    consumer = KafkaConsumer(topic,bootstrap_servers=['20.219.122.194:9092'], auto_offset_reset = "latest", value_deserializer=lambda m: json.loads(m.decode("utf-8")))

    for message in consumer:
        print(message.value)
        return (message.value)["value"]
    
    return -9999.0

    # 

    # print("In getSensor data in api.py")
    # print(data)
    # for each in data:
    #     # print("each",each)
    #     if(each['type'] == sensor_type and int(each['serial_num']) == serial_num):
    #         sensor_topic = each['topic']
    #         print(sensor_topic)
    #         consumer = KafkaConsumer(sensor_topic, auto_offset_reset='latest',
    #                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    #         for message in consumer:
    #             print(message.value)
    #             return message.value
    if sensor_type=="float":
        return 1.5
    else :
        return "string"

def predict(data,modelName):
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col = dbname['model_nodes']

    query = {"model":modelName}
    d = col.find(query)
    
    ip=""
    port=""
    for x in d:
        ip,port = x['ip'],x['port']
    print(ip,port)

    endpoint = "http://"+ip+":"+str(port)+"/predict"
    print(endpoint)
    # endpoint = "http://localhost:5036/predict"
    reply = requests.post(endpoint,json = data)
    
    return reply.text                   

def controller(predicted_data):
    print(predicted_data)

# data = getSensorData("light-sensor", 0, "app1")

# print(data)

