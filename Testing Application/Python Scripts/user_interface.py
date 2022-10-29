import re
from pandas import date_range
import requests
import json

session = requests.Session()

print("\n<<---- Welcome User ---->>\n")


def titanic():
    while True:
        print("Let's guess you'd have survived the Titanic Disaster or not..")

        sex = int(
            input("Enter the Gender ('0' OR '1')) : \n1 - Male \n0 - Female \n>>> "))

        fare = float(
            input("Enter the Fare of the Ticket (Integer between 0-512) :\n>>> "))

        age = float(input("Enter Age : \n>>> "))

        pclass = int(input(
            "Enter Class of Ticket('1' OR '2' OR '3') : \n1 - 1st Class \n2 - 2nd Class \n3 - 3rd Class\n>>>"))

        embarked = int(
            input("Enter the stop you Embarked upon ('1' OR '2' OR '3') : \n1 - Cherbourg \n2 - Queenstown \n3 - Southampton \n>>> "))

        data = {
            "Sex": sex,
            "Fare": fare,
            "Age": age,
            "Pclass": pclass,
            "Embarked": embarked
        }

        response = session.post(
            "http://localhost:8080//titanic_model", json=data).content.decode("utf-8")
        print(response)

        check = input("\nType 'Y' to try again else enter 'N' \n>>>")
        if check == "N":
            break
        elif check == "Y":
            continue
        else:
            print("Invalid Input..\n<Exiting>")
            break


def salary():
    while True:
        print("Let's predict your salary on the basis of your work experience..")

        exp = float(input("Enter your experience in years : \n"))

        data = {"years": exp}

        response = session.post(
            "http://localhost:8080//salary_model", json=data).content.decode("utf-8")

        print(response)

        check = input("\nType 'Y' to try again else enter 'N' \n>>>")
        if check == "N":
            break
        elif check == "Y":
            continue
        else:
            print("Invalid Input..\n<Exiting>")
            break


def sales():
    while True:
        print("Let's predict your sales in 3rd month..")

        rate = int(input("Enter your rate of interest : "))
        sale1 = int(input("Enter your sales in 1st month : "))
        sale2 = int(input("Enter your sales in 2nd month : "))

        data = {"rate": rate, "first": sale1, "second": sale2}

        response = session.post(
            "http://localhost:8080//sales_model", json=data).content.decode("utf-8")

        print(response)

        check = input("\nType 'Y' to try again else enter 'N' \n>>>")
        if check == "N":
            break
        elif check == "Y":
            continue
        else:
            print("Invalid Input..\n<Exiting>")
            break


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

        class_type = "as"
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


print("Select Model : \n1. Salary Prediction \n2. Titanic Survival \n3. Predict Sales \n4. Wine Classification")
choice = int(input())

if choice == 1:
    salary()

if choice == 2:
    titanic()

if choice == 3:
    sales()

if choice == 4:
    wine()
