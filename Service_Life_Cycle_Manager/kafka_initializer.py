from grpc import server
import sys

vm_ip = sys.argv[1]

# line28 = "\tlisteners = listener_name://20.219.122.194:9092\n"
# line30 = "\tlisteners = PLAINTEXT://20.219.122.194:9092\n"
line36 = "advertised.listeners=PLAINTEXT"+vm_ip[4:20]+":9092\n"
line31 = "listeners=PLAINTEXT://0.0.0.0:9092\n"

with open('Kafka/config/server.properties', 'r', encoding='utf-8') as file:
    data = file.readlines()

# data[27] = line28
# data[29] = line30
data[30] = line31
data[35] = line36

with open("Kafka/config/server.properties", 'w', encoding='utf-8') as file:
    file.writelines(data)

print("Done")


# 20.219.122.194




# file = open("server.properties", "r")
# replacement = ""
# # using the for loop
# i=1
# for line in file:
#     if(i==28):
#         line = line.strip()
#         # changes = line.replace("hardships", "situations")
#         line = line28
#         replacement = replacement + line28
#     elif(i==30):
#         line = line.strip()
#         # changes = line.replace("hardships", "situations")
#         line = line30
#         replacement = replacement + line30


#     elif(i==36):
#         line = line.strip()
#         # changes = line.replace("hardships", "situations")
#         line = line36
#         replacement = replacement + line36

#     else:
#         replacement = replacement + line



    

# file.close()
# # opening the file in write mode
# fout = open("server1.properties", "w")
# fout.write(replacement)
# fout.close()
