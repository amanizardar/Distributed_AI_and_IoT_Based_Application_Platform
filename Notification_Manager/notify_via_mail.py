from crypt import methods
from flask import Flask
from flask_mail import Mail, Message
from flask import request
   
app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'team7.ias@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ashu@2904'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   
# message object mapped to a particular URL ‘/’
@app.route("/",methods=['POST'])
def index():
   msg_title = request.json['title']
   msg_content = request.json['content']
   email = request.json['email_id']
   print(msg_title,msg_content) 
   msg = Message(
                msg_title,
                sender ='team7.ias@gmail.com',
                recipients = [email]
               )
   msg.body = msg_content
   mail.send(msg)
   return 'Sent'


@app.route("/healthCheck", methods=['GET', 'POST'])
def healthCheck():
    return "ok"
    
if __name__ == '__main__':
   app.run(host="0.0.0.0",port=8765,debug = True)