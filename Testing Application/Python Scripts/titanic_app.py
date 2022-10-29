import requests
import json

session = requests.Session()


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
