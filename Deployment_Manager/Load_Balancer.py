import paramiko
from pymongo import MongoClient
import time

def choose_best_node():
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    col = dbname["VM_DETAILS"]
    myquery = { "status": "active" }
    vm_data = col.find(myquery)
    stats = []
    c = 0
    for i in vm_data:
        cpu,ram = check(i['username'], i['password'], i['ip'])
        # if ram > some_value //TO_DO
        print(cpu,ram)
        stats.append([cpu,ram,i['username'], i['password'], i['ip']])
        
    n=len(stats)
    stats.sort()

    i = 0
    while i<n-1 and stats[i][0] == stats[i+1][0]:
        i += 1
    #print(stats[i])
    # i['username'], i['password'], i['ip']
    return stats[i][2],stats[i][3],stats[i][4] 


def check(username, password, hostname):
    # username = "azureuser"
    # password = "@mazingSpiderMan"
    # hostname = "20.74.248.92"
    port = 22 
    #print(username,password,hostname)
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, port, username, password)
    stdin,stdout,stderr = s.exec_command("free | tail -2 | head -1 | awk '{print $4}'")
    ram = stdout.readline()
    stdin,stdout,stderr = s.exec_command('vmstat 1 2 | tail -1')
    cpu = stdout.readline()
    cpu = cpu.split()
    ram = ram[:-1]
    ram = int(ram)
  #  print(cpu,ram)
    cpu_usage = 100-float(cpu[14])
    return cpu_usage,ram
