import requests
import json


def user_location(ip):
        url = f"http://ip-api.com/json/{ip}"

        response = requests.get(url=url)
        valid = json.loads(response.text)

        return valid
