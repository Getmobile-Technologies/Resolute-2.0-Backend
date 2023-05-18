from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
import string
import random

def generate_password():
    a = []
    for _ in range(4):
        a.append(random.choice(string.digits))
    random.shuffle(a)
    return "".join(a)


def generate_admin_password():
    a = []
    for _ in range(4):
        a.append(random.choice(string.digits))
    random.shuffle(a)
    pin = "".join(a)
    return "resolute" + pin


def split(str):
    list = str.split(",")
    return list[0]


def phone_authenticate(self, request, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone=phone)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            raise AuthenticationFailed(detail="password don't match")
