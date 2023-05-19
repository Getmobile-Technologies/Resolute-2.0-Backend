import nexmo
import vonage
import os
import requests
from main.models import PanicRequest
import urllib.parse

Vonage_API_Key = os.getenv("vonage_api_key")
Vonage_API_Secret = os.getenv("vonage_secret_key")
api_key = os.getenv("api_key_2")


nexmo_client = vonage.Client(
    key=Vonage_API_Key, secret=Vonage_API_Secret
)
sms = vonage.Sms(nexmo_client)

def geocoding(lat, long):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{long}",
        "key": f"{api_key}"
    }
    response  = requests.get(url=url, params=params)
    result = response.json()['results'][0]
    address = result['formatted_address']

    base_url = "https://www.google.com/maps/search/?api=1"
    params2 = {
        "query": address,

    }

    mapped_url = base_url + '&' + urllib.parse.urlencode(params2)

    return mapped_url


def sign_up_sms(number, pin):
    message = f"""
    Hello!, your account as been created by the admin.
    Your login details are;
    Phone: {number}
    PIN: {pin}
    Thank you!.
    """
    request = sms.send_message({
        "from": "Resolute",
        "to": number,
        "text": message
    })


    return request
    

def emergency_sms(panic:PanicRequest, phone):
    url = geocoding(lat=panic.latitude, long=panic.longitude)

    message = f"""{panic.user.first_name.title()} from {panic.location} just made a panic alert.
The situation should be attended to immediately.
see location: {url},
Call: {panic.user.phone}"""
    request = sms.send_message({
        "from": "Resolute",
        "to": phone,
        "text": message
    })

    return request