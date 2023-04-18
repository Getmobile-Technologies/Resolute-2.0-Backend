import requests
import json


def user_location():
        url = "http://ip-api.com/json/"

        response = requests.get(url=url)
        valid = json.loads(response.text)

        return valid
