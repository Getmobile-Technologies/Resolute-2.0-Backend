import nexmo
import vonage
import os

Vonage_API_Key = os.getenv("vonage_api_key")
Vonage_API_Secret = os.getenv("vonage_secret_key")


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
    

def emergency_sms(location, long, lat, emergency_con):
    message = f"""
    EMERGENCY!!!!
    A panic request as been made at {location}.
    The situation should be attended to immediately.
    User coordinates http://www.google.com/maps/place/{long},{lat}
    """
    request = sms.send_message({
        "from": "Resolute",
        "to": emergency_con,
        "text": message
    })

    return request