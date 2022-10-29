from pymongo import MongoClient

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']

IP_ADDRESSES = dbname["MODULE_URL"]
ip_table = IP_ADDRESSES.find_one({'name': 'Request_Manager'})
print(ip_table['url'])

IP_ADDRESSES.update_one({'name': 'Request_Manager'},{ '$set':{'url':"123"} })

ip_table = IP_ADDRESSES.find_one({'name': 'Request_Manager'})
print(ip_table['url'])
# REQUEST_MANAGER =  ip_table['REQUEST_MANAGER']['url']
# SENSOR_CONFIGURER = ip_table['SENSOR_CONFIGURER']['url']
      
    