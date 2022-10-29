import requests
import json

session = requests.Session()


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
