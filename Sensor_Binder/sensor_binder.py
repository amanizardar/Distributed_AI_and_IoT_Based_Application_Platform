import json
import threading
# from kafka import KafkaConsumer
from pymongo import MongoClient
# from data_generator_kafka_producer import *

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']
SENSOR_INSTANCES_DB = dbname["SENSOR_INSTANCES"]


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
            print(sensorInstances[j]['type'],sensorInstances[j]['location'])  
            if sensorInstances[j]['type'] == i['type'] and sensorInstances[j]['location'] == i['location'] and busy_sensor_map[j] == 0:
                busy_sensor_map[j] = 1
                count = alotted_sensors.get(currentSensorReq, 0)
                alotted_sensors[currentSensorReq] = count+1

                key = currentSensorReq + str(count)
                # print(key)
                topic_id =str(sensorInstances[j]['_id'])+"_topic"
                val = {"type": sensorInstances[j]['type'] , "location" : sensorInstances[j]['location'], "topic" : topic_id, "serial_num" : i["serial_num"]}
                binding_map.append(val)
                sensorAvailable = True
                break

        if not sensorAvailable:
            print("Error: Sensor not available!")
            return
    # print(binding_map)
    return binding_map
