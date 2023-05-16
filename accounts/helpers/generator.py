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

