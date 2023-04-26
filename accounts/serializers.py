from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from main.models import StaffLocation
from django.contrib.auth import get_user_model
User = get_user_model()



class UserRegisterationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=100, default='staff')
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    email = serializers.CharField(max_length=200, required=False)
    location = serializers.PrimaryKeyRelatedField(queryset=StaffLocation.objects.all(), required=False)

    class Meta():
        model = User
        fields = ['id', "first_name", "last_name", "phone", "email", 'location', "role", "password"]

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class AdminRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=100, default='admin')
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    location = serializers.PrimaryKeyRelatedField(queryset=StaffLocation.objects.all(), required=False)
    total_admin_panic = serializers.ReadOnlyField()


   
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone", "email", "location", "total_admin_panic", "role", "password"]

    def create(self, validate_data):
        return User.objects.create_admin(**validate_data)

class SuperAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    location = serializers.PrimaryKeyRelatedField(queryset=StaffLocation.objects.all(), required=False)

   
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone", "email", "location", "role", "password"]

    def create(self, validate_data):
        return User.objects.create_superuser(**validate_data)



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=700)
    password = serializers.CharField(max_length=700)

   
class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=700)
    password = serializers.CharField(max_length=700)



class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:

        	return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

