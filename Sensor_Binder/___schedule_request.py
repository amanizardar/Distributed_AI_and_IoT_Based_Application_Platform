# from crypt import methods
# from flask import Flask, request, render_template
# import threading
# from flask import flash
# from pymongo import MongoClient
# import schedule
# import time
# import datetime

# app = Flask(__name__)

# scheduling_data =""

# @app.route("/schedule_data", methods=['POST'])
# def receive_binding_map():
#     global scheduling_data
#     scheduling_data = request.json
#     return str(scheduling_data)

# def writelog(msg):
#     f = open("schedulerLog.txt", "a")
#     msg=msg+"\n"
#     f.write(msg)
#     f.close()

# def sendToDeployer (data,repeatStatus, operation):
#     msg="Request from username: "+data['username']+" to start service sent to deployer"
#     writelog(msg)
#     if(operation == "start"):
#         print("Forwarding start request to the Deployer")
#         # response=requests.post("{{URL}}/startRequest",json=scheduling_data).content.decode()
#     else:
#         print("Forwarding stop request to the Deployer")
#         # response=requests.post("http://127.0.0.1:5005/stopRequest",json=scheduling_data).content.decode()

#     if(repeatStatus=='False'):
#         return schedule.CancelJob

# def everydaySchedule(data):
#     schedule.every().day.at(data['StartTime']).do(sendToDeployer,data,True)

# def repeatSchedule(data, repeatStatus):
#     daysData=data['days']
#     msg="Scheduled Request from username: "+data['username']+" for every "
#     msgdash="Scheduled to kill request from username: "+data['username']+" for every "

#     for days in daysData:
#         if(days == 'monday'):
#             schedule.every().monday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Monday")
#             schedule.every().monday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus,"end")
#             writelog(msgdash+"Monday")

#         elif(days=='tuesday'):
#             schedule.every().tuesday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Tuesday")
#             schedule.every().tuesday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Tuesday")

#         elif(days=='wednesday'):
#             schedule.every().wednesday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Wednesday")
#             schedule.every().wednesday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Wednesday")

#         elif(days=='thursday'):
#             schedule.every().thursday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Thursday")
#             schedule.every().thursday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Thursday")

#         if(days=='friday'):
#             schedule.every().friday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Friday")
#             schedule.every().friday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Friday")

#         if(days=='saturday'):
#             schedule.every().saturday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Saturday")
#             schedule.every().saturday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Saturday")

#         if(days=='sunday'):
#             schedule.every().sunday.at(data['StartTime']).do(sendToDeployer,data,repeatStatus,"start")
#             writelog(msg+"Sunday")
#             schedule.every().sunday.at(data['EndTime']).do(sendToDeployer, data, repeatStatus, "end")
#             writelog(msgdash+"Sunday")

# def scheduleRequest(data):
#     if len(data['days']) == 7:
#         everydaySchedule(data)                  # Daily job
#     else:
#         repeatSchedule(data,data['repeat'])     

# def formatFormData(output):
#     currentTimeDate = datetime.datetime.now()
#     currentTime = currentTimeDate.strftime('%H:%M')

#     data = {'username': '', 'token':'', 'user_type':'', 'days': [], 'StartTime': currentTime, 'EndTime': (currentTimeDate + datetime.timedelta(seconds = 100)).strftime('%H:%M'), 'repeat': False}
#     if 'username' in output:
#         data['username'] = output['username']

#     # if 'ApplicationID' in output:
#     #     data['ApplicationID'] = output['ApplicationID']

#     if 'StartTime' in output and output['StartTime'] != "":
#         data['StartTime'] = output['StartTime']

#     if 'EndTime' in output and output['EndTime'] != "":
#         data['EndTime'] = output['EndTime']

#     for i in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
#         if i in output:
#             data['days'].append(i.lower())

#     if(len(data['days'])==0):
#         data['days']=['Sunday']
    
#     if 'repeat' in output:
#         data['repeat']=True

#     return data


# @app.route("/submitSchedule", methods=["POST", "GET"])
# def submitSchedule():
#     output = request.form.to_dict()
#     data=formatFormData(output)
#     print(data)
#     scheduleRequest(data)
#     return render_template("scheduler_frontend.html")


# def runPending():
#     # pick task from DB and run it
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# def renderUI():
#     app.use_reloader=False
#     app.run(port=5005)

# t1 = threading.Thread(target=renderUI)
# t2 = threading.Thread(target = runPending)

# t1.start()
# t2.start()

# t1.join()
# t2.join()