import random
        
        
def generate_code() -> str:
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    otp = "".join(str(random.choice(digits)) for _ in range(4))
    return otp
