from flask import Flask, request, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import requests
import datetime
import jwt
from pymongo import MongoClient

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# db = client.flask_db
# todos = db.todos
CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SECRET_KEY'] = 'secretkey'

# db = SQLAlchemy(app)

# class User():
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     def  encode_auth_token(self, user_id):
#         print("encode yes man")
#         try:
#             payload = {
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
#                 'iat': datetime.datetime.utcnow(),
#                 'sub': user_id
#             }
#             return jwt.encode(
#                 payload,
#                 app.config.get('SECRET_KEY'),
#                 algorithm='HS256'
#             )
#         except Exception as e:
#             print("some error yes man")
#             return e

def  encode_auth_token(user_id):
        print("encode yes man")
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print("some error yes man")
            return e

# class App_Developer(User, db.Model):
#     __tablename__ = 'app_developer'

# class Data_Scientist(User, db.Model):
#     __tablename__ = 'data_scientist'

# class End_User(User, db.Model):
#     __tablename__ = 'end_user'

# userDict = {
#         "App_Developer": App_Developer,
#         "Data_Scientist": Data_Scientist,
#         "End_User": End_User
#     }
# UserDict_MONGO = {
#     "Data_Scientist" : dbname["Data_Scientist"], 
#     "App_Developer" : dbname["App_Developer"],
#     "End_User" :  dbname["End_User"],
#     "Platform_Configurer" :  dbname["Platform_Configurer"]
# }

@app.route('/create_user/<user_type>', methods = ['POST'])
def do_signup(user_type):
    print("spider man")
    if(request.method=='POST'):
        print("super man")
        data = request.get_json()
        user = {
            'username': data['username'],
            'password': data['password']
        }

        # #########SQLLITE
        # temp_user = userDict[user_type].query.filter_by(username=user['username']).first()
        # if(temp_user is not None):
        #     print("idiot man")
        #     responseObject = {
        #         'status': 'Failed',
        #         'message': "User already registered, please sign in"
        #     }
        #     return make_response(jsonify(responseObject)), 409
        # else:
        #     print("yes man")
        #     user = userDict[user_type](username=user['username'], password=user['password'])
        #     db.session.add(user)
        #     db.session.commit()
        #     auth_token = user.encode_auth_token(user.id)
        #     responseObject = {
        #         'status': 'Success',
        #         'message': "Success",
        #         'auth_token': auth_token
        #     }
        #     return make_response(jsonify(responseObject)), 200


        mongo_user = dbname[user_type].find_one({'username' : user["username"]})
        #print(mongo_user['_id'])
        
        if(mongo_user is not None):
            print("idiot man")
            responseObject = {
                'status': 'Failed',
                'message': "User already registered, please sign in"
            }
            return make_response(jsonify(responseObject)), 409
        else:
            print("yes man")
            user_m = dbname[user_type].insert_one(user)
            
            auth_token = encode_auth_token(str(user['username']) )
            responseObject = {
                'status': 'Success',
                'message': "Success",
                'auth_token': auth_token
            }
            return make_response(jsonify(responseObject)), 200

@app.route('/authenticate_user/<user_type>', methods = ['GET', 'POST'])
def authenticate(user_type):
    if(request.method=='POST'):
        data = request.get_json()
        #user_type = request.args.get('user_type')
        user = {
            'username': data['username'],
            'password': data['password']
        }
        
        # #############SQLLITE
        # user = userDict[user_type].query.filter_by(username=user['username']).first()
        # if(user is not None):
        #     if(user.password == password):
        #         #login_user(user)
        #         auth_token = user.encode_auth_token(user.id)
        #         if auth_token:
        #             responseObject = {
        #                 'status': 'Success',
        #                 'message': 'Success',
        #                 'auth_token': auth_token
        #             }
        #         return make_response(jsonify(responseObject)), 200
        #     else:
        #         responseObject = {
        #                 'status': 'Failed',
        #                 'message': "Incorrect Password"
        #             }
        #         return make_response(jsonify(responseObject)), 401
        # else:
        #     responseObject = {
        #             'status': 'Failed',
        #             'message': "No such User exists"
        #         }
        #     return make_response(jsonify(responseObject)), 401

        temp_user = dbname[user_type].find_one({'username':user['username']})
        if(temp_user is not None):
            print(str(temp_user['username']))
            if(user['password'] == temp_user['password']):
                #login_user(user)
                auth_token = encode_auth_token(str(temp_user['username']))
                if auth_token:
                    responseObject = {
                        'status': 'Success',
                        'message': 'Success',
                        'auth_token': auth_token
                    }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                        'status': 'Failed',
                        'message': "Incorrect Password"
                    }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                    'status': 'Failed',
                    'message': "No such User exists"
                }
            return make_response(jsonify(responseObject)), 401

@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"

if(__name__ == '__main__'):
    # db.create_all()
    # userDict = {
    #     "App_Developer": App_Developer,
    #     "Data_Scientist": Data_Scientist,
    #     "End_User": End_User
    # }
    app.run(host ='0.0.0.0',port=5001,debug=True)
    