from pymongo import MongoClient

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

dbname = client['AI_PLATFORM']

col = dbname["VM_DETAILS"]

data = [{"name":"IASVMHackathon","ip": "20.213.161.182","username": "IASHackathon1","password":"IASHackathon1","status":"active","first_free_port":5000},
        {"name":"iasVM1","ip": "20.219.122.194","username": "iasVM12345678","password":"iasVM12345678","status":"inactive","first_free_port":5000},
        {"name":"","ip": "20.233.44.84","username": "azureuser","password":"r00tPa$$w0rd278","status":"inactive","first_free_port":5000}]

for i in data:
    a = col.insert_one(i)
