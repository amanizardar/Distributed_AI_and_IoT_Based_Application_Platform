# from re import template
# import certifi
# import ast
# from pymongo import MongoClient
# from flask import Flask, render_template, request

# app = Flask(__name__)

# CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
# client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

# dbname = client['Application']
# app_req_db = dbname["app_requirement"]


# @app.route("/sensor_location", methods=['POST', 'GET'])
# def sensor_requirements():
#     app_sensor_data = {}
#     sensor_kinds = list()
#     sensor_count = list()

#     selectedApp = request.form.to_dict()

#     for i in selectedApp:
#         given_app_id = i
#         print(i)

#     sensors_req = list(app_req_db.find())

#     for app_instance in sensors_req:
#         if app_instance["app_id"] == given_app_id:
#             app_sensor_data = app_instance

#     if app_sensor_data == {}:
#         print("Error : App ID not found")
#     else:
#         print("Application sensor requirements are : ",
#               app_sensor_data["sensors"])

#     app_sensor_req = ast.literal_eval(app_sensor_data["sensors"])

#     for sensor_type in app_sensor_req:
#         sensor_kinds.append(sensor_type)
#         sensor_count.append(app_sensor_req[sensor_type])

#     return render_template("sensor_location.html", sensor_kinds=sensor_kinds, sensor_count=sensor_count)


# if __name__ == "__main__":
#     app.run(port=6005, debug=True)
