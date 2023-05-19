import nexmo
import vonage
import os
from main.models import PanicRequest

Vonage_API_Key = os.environ.get("vonage_api_key")
Vonage_API_Secret = os.environ.get("vonage_secret_key")


nexmo_client = vonage.Client(
    key=Vonage_API_Key, secret=Vonage_API_Secret
)
sms = vonage.Sms(nexmo_client)

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
    message = f"""{panic.user.first_name.title()} from {panic.location} just made a panic alert.
The situation should be attended to immediately.
see location: http://www.google.com/maps/place/{panic.longitude},{panic.latitude},
Call: {panic.user.phone}"""
    request = sms.send_message({
        "from": "Resolute",
        "to": phone,
        "text": message
    })

    return request