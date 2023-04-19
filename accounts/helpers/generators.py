import random
        
        
def generate_code() -> str:
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    otp = "".join(str(random.choice(digits)) for _ in range(4))
    return otp


# class ClientIPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip_address = x_forwarded_for.split(',')[0]
#         else:
#             ip_address = request.META.get('REMOTE_ADDR')
#         request.client_ip_address = ip_address
#         response = self.get_response(request)
#         return response





