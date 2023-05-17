from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from phonenumber_field.serializerfields import PhoneNumberField
from .models import UserActivity, Organisations
from main.models import StaffLocation
from django.contrib.auth import get_user_model
User = get_user_model()



class UserRegisterationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=100, default='staff')
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)
    email = serializers.CharField(max_length=200, required=False)
    location = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    organisation = serializers.CharField(required=True)
    open_password = serializers.CharField(required=False)
    state = serializers.CharField(required=True)

    class Meta():
        model = User
        fields = ['id', "first_name", "last_name", "phone", "email", 'location', "state", "organisation", "role", "password", "open_password"]

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class AdminRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=100, default='admin')
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)
    location = serializers.CharField(required=False)
    organisation = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone", "email", "location", "role", "organisation", "password"]

    def create(self, validate_data):
        return User.objects.create_admin(**validate_data)

class SuperAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    location = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)


   
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
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=300)
    phone = serializers.CharField(required=False)





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



class ActivitySerializer(serializers.ModelSerializer):

    class Meta:

        model = UserActivity
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisations
        fields = '__all__'


class CreateOrganisationSerializer(serializers.Serializer):
    admin = AdminRegistrationSerializer()
    organisation = OrganisationSerializer()