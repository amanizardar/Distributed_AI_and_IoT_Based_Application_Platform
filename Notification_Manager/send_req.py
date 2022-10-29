import requests

json_data = {'title':'IAS','content':'Hello IAS Team 7!','email_id':'heyayushh@gmail.com'}
ret = requests.post(url="http://127.0.0.1:5000",json=json_data)