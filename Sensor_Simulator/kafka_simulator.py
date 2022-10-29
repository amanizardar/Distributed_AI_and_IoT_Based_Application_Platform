#from matplotlib.font_manager import json_dump
from pymongo import MongoClient
from kafka import KafkaProducer
import random
import json
import string
import schedule
import threading
import time

# CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
CONNECTION_STRING = "mongodb+srv://root:root@cluster0.llzhh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']
SENSOR_INSTANCES_DB = dbname["SENSOR_INSTANCES"]
SENSOR_INFO_DB = dbname["SENSOR_INFO"]
MODULE_URL_DB = dbname["MODULE_URL"]

def float_generator():
    return random.uniform(3, 130)


def string_generator():
    return str(''.join(random.choices(string.ascii_letters, k=random.randint(3, 15))))



def produce(sensor_instance_id,data_format):
    if data_format == 'float':
        x = float_generator()
        data = {
            "format" : "float",
            "value" : str(x)
        }
    elif data_format == 'string':
        x = string_generator()
        data = {
            "format" : "str",
            "value" : str(x)
        }

    KAFKA_IP = list(MODULE_URL_DB.find({"name" : "Kafka"}))[0]["url"][7:][:-5]
    print(KAFKA_IP)
    topic_name = str(sensor_instance_id)+"_topic"
    producer = KafkaProducer(bootstrap_servers= KAFKA_IP+':9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        
    # topic_name = str(sensor_instance_id)+"_topic"
    # producer = KafkaProducer(bootstrap_servers='20.219.122.194:9092',
    #                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(topic_name,data)
    print("Produced ",x," on: ", sensor_instance_id)


def runPending():
    # pick task from DB and run it
    print("In Run Pending")
    while True:
        schedule.run_pending()
        time.sleep(1)


def startProduction():
    sensor_instances = list(SENSOR_INSTANCES_DB.find())
    for instance in sensor_instances:
        print(instance)
        d = list(SENSOR_INFO_DB.find({"type" : instance['type']}))[0]
        data_format = d['input_format']
        data_rate = d['data_rate']
        sensor_instance_id = str(instance['_id'])
        schedule.every(int(data_rate)).seconds.do(produce,sensor_instance_id,data_format)

t1 = threading.Thread(target = startProduction)
t2 = threading.Thread(target = runPending)

t1.start()
t2.start()

t1.join()
t2.join()

# for every instance in binding_map
# get sensor type from object id
# get output format from sensor type
# call generate_type function
# produce into topic (objectid + '_topic')
