#from matplotlib.font_manager import json_dump
from pymongo import MongoClient
from kafka import KafkaProducer, KafkaConsumer
import random
import json
import string

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']
IP_ADDRESSES = dbname["MODULE_URL"]
all_instances = dbname["SENSOR_INSTANCES"]
sensor_info = dbname["SENSOR_INFO"]



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
    
    topic_name = str(sensor_instance_id)+"_topic"
    kafka_ip = IP_ADDRESSES.find_one({'name': 'Kafka'})['url']
    start = kafka_ip.find("/")+2
    end = kafka_ip.rfind(":")
    producer = KafkaProducer(bootstrap_servers=kafka_ip[start:end]+':9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        
    producer.send(topic_name,data)
    print("Produced ",x," on: ", sensor_instance_id)

# for every instance in binding_map
# get sensor type from object id
# get output format from sensor type
# call generate_type function
# produce into topic (objectid + '_topic')
