import json
import sys

def dockerGenerator(config_file_path, service_name):
    configFile = open(config_file_path,'r')
    config = json.load(configFile)
    configFile.close()

    print("Inside application docker generator.")
    print(config)

    df = open('Dockerfile','w')
    print("inside docker generation")

    str = "FROM python:3\nCOPY . /app\nWORKDIR /app\n"


    app_config = config['Application']

    # for key,service in all_services.items():
        
    if app_config['appName'] == service_name:
        dependencies = app_config['dependencies']#list
        filenames = app_config['filenames']#list

        # for ev_key,ev_val in service['environment'].items():
        #     if ev_val:
        #         if ev_key == 'flask':
        #             str += 'RUN pip3 install flask\n\n'

                # to-do for more tech
        # entry_point = config['Application']['entryPoint']#string
    

        for dependency in dependencies:
            str += "RUN pip3 install " + dependency + "\n"

        # for filename in filenames:
        #     str += "ADD " + filename + " .\n"
    
        #for dynamically fetching Kafka URL
        str += "RUN pip3 install pymongo\n"    
    
        str+='CMD ["python3","-m","flask","run","--host=0.0.0.0"]'
        print(str)
    df.write(str)
    df.close()

# config file, service name
dockerGenerator(sys.argv[1], sys.argv[2])

# dockerGenerator("./config.json","service-1")