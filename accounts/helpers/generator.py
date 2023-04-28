import string
import random

def generate_password():
    a = []
    for _ in range(4):
        a.append(random.choice(string.digits))
    random.shuffle(a)
    return "".join(a)