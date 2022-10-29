import requests
import json

session = requests.Session()


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
