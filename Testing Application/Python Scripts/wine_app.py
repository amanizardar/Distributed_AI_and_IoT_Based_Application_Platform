import requests
import json

session = requests.Session()


def wine():
    while True:
        data = [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8,
                 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]]

        print("Let's see what readings of sensors are..")

        print(data, "\n")

        j_data = json.dumps(data)

        headers = {'content-type': 'application/json',
                   'Accept-Charset': 'UTF-8'}

        response = requests.post(
            "http://localhost:8080//wine_model", data=j_data, headers=headers)

        class_type = "null"
        if response.text == "1.0":
            class_type = "Class 1"
        elif response.text == "2.0":
            class_type = "Class 2"
        if response.text == "3.0":
            class_type = "Class 3"

        print("Given wine belongs to : ", class_type)

        check = input("\nType 'Y' to try again else enter 'N' \n>>>")
        if check == "N":
            break
        elif check == "Y":
            continue
        else:
            print("Invalid Input..\n<Exiting>")
            break
