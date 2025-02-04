import nexmo
import vonage
import os
import requests
from main.models import PanicRequest, CallRequest
import urllib.parse
from twilio.rest import Client
import logging

# Vonage_API_Key = os.getenv("vonage_api_key")
# Vonage_API_Secret = os.getenv("vonage_secret_key")
api_key = os.getenv("GEO_API_KEY")


# nexmo_client = vonage.Client(
#     key=Vonage_API_Key, secret=Vonage_API_Secret
# )
# sms = vonage.Sms(nexmo_client)



account_sid = os.getenv('TWILIO_ID')
auth_token = os.getenv('TWILIO_TOKEN')
client = Client(account_sid, auth_token)



def geocoding(lat, long):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{long}",
        "key": api_key
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
    # request = sms.send_message({
    #     "from": "Resolute",
    #     "to": number,
    #     "text": message
    # })

    try:
        res = client.messages.create(
        from_="Resolute",
        body=message,
        to=number
            )
    except Exception as e:

        logging.error("An error occurred: %s", str(e))
        return


    return res
    

def emergency_sms(panic:PanicRequest, phone):
    url = geocoding(lat=panic.latitude, long=panic.longitude)

    message = f"""{panic.user.first_name.title()} from {panic.location} just made a panic alert.
The situation should be attended to immediately.
see location: {url},
Call: {panic.user.phone}"""
    # request = sms.send_message({
    #     "from": "Resolute",
    #     "to": phone,
    #     "text": message
    # })
    try:
        res = client.messages.create(
        from_="Resolute",
        body=message,
        to=phone
        )
    except Exception as e:

        logging.error("An error occurred: %s", str(e))
        return


    return res



def call_emergency_sms(panic:CallRequest, phone):

    message = f"""{panic.user.first_name.title()} from {panic.user.location} just made a distress call request.
The situation should be attended to immediately.
Call: {panic.phone}"""
    # request = sms.send_message({
    #     "from": "Resolute",
    #     "to": phone,
    #     "text": message
    # })

    try:
        res = client.messages.create(
        from_="Resolute",
        body=message,
        to=phone
        )
    except Exception as e:

        logging.error("An error occurred: %s", str(e))
        return


    return res