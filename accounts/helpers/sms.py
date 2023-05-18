import nexmo
import os

Vonage_API_Key = os.getenv("vonage_api_key")
Vonage_API_Secret = os.getenv("vonage_secret_key")


nexmo_client = nexmo.Client(
    api_key=Vonage_API_Key, api_secret=Vonage_API_Secret
)
Vonage_number = os.getenv("vonage_number")

def sign_up_sms(number, pin):
    message = f"""
    Hello!, your account as been created by the admin.
    Your login details are;
    Phone: {number}
    PIN: {pin}
    Thank you!.
    """
    request = nexmo_client.send_message({
        "from": Vonage_number,
        "to": number,
        "message": message
    })

    return request