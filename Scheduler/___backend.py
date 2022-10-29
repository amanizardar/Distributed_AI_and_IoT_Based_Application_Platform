# from flask import Flask,redirect, request, render_template
# import threading
# from flask import flash
# from pymongo import MongoClient
# import schedule
# import time
# import datetime
# app = Flask(__name__)

# REQUEST_MANAGER = "http://127.0.0.1:5000"


# def formatFormData(output):
#     currentTimeDate = datetime.datetime.now()
#     currentTime = currentTimeDate.strftime('%H:%M')

#     data = {'userID': '', 'ApplicationID': '', 'days': [], 'StartTime': currentTime, 'Duration': 24*60, 'filename': None, 'repeat': False}
#     if 'userID' in output:
#         data['userID'] = output['userID']

#     if 'ApplicationID' in output:
#         data['ApplicationID'] = output['ApplicationID']

#     if 'StartTime' in output and output['StartTime'] != "":
#         data['StartTime'] = output['StartTime']

#     if 'Duration' in output and output['Duration'] != "":
#         data['Duration'] = output['Duration']

#     for i in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
#         if i in output:
#             data['days'].append(i.lower())

#     if(len(data['days'])==0):
#         data['days']=['Sunday']

#     if 'filename' in output:
#         data['filename'] = output['filename'] 
    
#     if 'repeat' in output:
#         data['repeat']=True

#     return data

# # CONNECTION_STRING = "mongodb+srv://root:root@cluster0.llzhh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
# client = MongoClient(CONNECTION_STRING)
# dbname = client['scheduler']
# collection_name = dbname["scheduling_requests"] 

# def writelog(msg):
#     f = open("schedulerLog.txt", "a")
#     msg=msg+"\n"
#     f.write(msg)
#     f.close()

# def everydaySchedule(data):
#     schedule.every().day.do(sendToDeployer,data,True)

# def repeatSchedule(data, repeatStatus):
#     daysData=data['days']
#     msg="Scheduled Request from userID: "+data['userID']+" for every "
#     for days in daysData:
#         if(days == 'monday'):
#             schedule.every().monday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Monday")
#         elif(days=='tuesday'):
#             schedule.every().tuesday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Tuesday")
#         elif(days=='wednesday'):
#             schedule.every().wednesday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Wednesday")
#         elif(days=='thursday'):
#             schedule.every().thursday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Thursday")
#         if(days=='friday'):
#             schedule.every().friday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Friday")
#         if(days=='saturday'):
#             schedule.every().saturday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Saturday")
#         if(days=='sunday'):
#             schedule.every().sunday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus)
#             writelog(msg+"Sunday")

# def sendToDeployer (data,repeatStatus):
#     msg="Request from userID: "+data['userID']+" sent to deployer"
#     writelog(msg)
#     print("Forwarding request to the Deployer")

#     if(repeatStatus=='False'):
#         collection_name.delete_one(data)
#         return schedule.CancelJob

# def scheduleRequest(data):
#     if len(data['days']) == 7:
#         everydaySchedule(data)                  # Daily job
#     else:
#         repeatSchedule(data,data['repeat'])     # Weekly or one time job

# def runPending():
#     # pick task from DB and run it
#     print("In Run Pending")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# @app.route("/toDB", methods=["POST", "GET"])
# def toDB():
#     print("In toDB")
#     output = request.form.to_dict()
#     print("received", output)
#     data=formatFormData(output)
#     collection_name.insert_one(data)

#     msg="Inserted into DB with userID: "+data['userID']
#     writelog(msg)
#     scheduleRequest(data)
#     stttr = REQUEST_MANAGER+"/Dashboard/"+output['user_type']
#     print(stttr) 
#     redir = redirect(REQUEST_MANAGER+"/Dashboard/"+output['user_type'])
#     redir.headers['Authorization'] = output['token']
#     return redir
#     #return render_template("temp.html")

# # app.run(port=5001)

# def renderUI():
#     app.use_reloader=False
#     app.run(port=5011)

# t1 = threading.Thread(target=renderUI)
# t2 = threading.Thread(target = runPending)

# # app.run(debug='True')

# t1.start()
# t2.start()

# t1.join()
# t2.join()