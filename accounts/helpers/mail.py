import requests
import os

key = os.getenv("email_key")
url = "https://resolute-admin-4-0.vercel.app/"
def signup_mail(email, password, first_name):
 
    requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}" 
        },
        json={
            "event": "sign",
            "email": email,
            "data": {
                "password": password,
                "url": url,
                "first_name": first_name
                }
            }
    )
