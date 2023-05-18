import nexmo
import vonage
import os

Vonage_API_Key = os.getenv("vonage_api_key")
Vonage_API_Secret = os.getenv("vonage_secret_key")


nexmo_client = vonage.Client(
    key=Vonage_API_Key, secret=Vonage_API_Secret
)
sms = vonage.Sms(nexmo_client)
Vonage_number = os.getenv("vonage_number")

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
    