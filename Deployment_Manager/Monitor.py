from pymongo import MongoClient
import Load_Balancer

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

dbname = client['AI_PLATFORM']

col1 = dbname["VM_DETAILS"]
col2 = dbname['model_nodes']

username, password, ip = Load_Balancer.choose_best_node()
print(ip)

myquery = { "ip": ip }
vm = col1.find(myquery)
port = 0
for i in vm:
    port = i["first_free_port"]
#print(port)
port += 1
col1.update_one({"ip":ip},{"$set":{"first_free_port":port}})

