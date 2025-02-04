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
    location_data = serializers.ReadOnlyField()
    organisation_data = serializers.ReadOnlyField()
    contact_admin_data = serializers.ReadOnlyField()

    class Meta():
        model = User
        fields = ["first_name", "last_name", "phone", "email", 'location', "role", "organisation", "location_data", "organisation_data", "contact_admin_data"]

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class AdminRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email", "role"]

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
    location_data = serializers.ReadOnlyField()
    organisation_data = serializers.ReadOnlyField()
    contact_admin_data = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = '__all__'
        
        
class UserDeleteSerializer(serializers.Serializer):
    current_password = serializers.CharField()

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
    total_registered_users = serializers.ReadOnlyField()
    total_incidence = serializers.ReadOnlyField()
    resolved_incidence = serializers.ReadOnlyField()
    unresolved_incidence = serializers.ReadOnlyField()
    ingenuine_incidence = serializers.ReadOnlyField()
    admin_data = serializers.ReadOnlyField()
    category_data = serializers.ReadOnlyField()
    

    class Meta:
        model = Organisations
        fields = '__all__'

 
class CreateOrganisationSerializer(serializers.Serializer):
    admin = AdminRegistrationSerializer()
    organisation = OrganisationSerializer()
    
    
    def update(self, validated_data, org, user):
        fields = org.__dict__
        # update locations
        organization = validated_data.get('organisation', {})
        
        # update product fields
        for field in fields:
            if field in organization:
                setattr(org, field, validated_data['organisation'][field])
        org.save()
        
        
        # Updating admin
        fields = user.__dict__
        # update locations
        admin = validated_data.get('admin', {})
        
        # update product fields
        for field in fields:
            if field in admin:
                setattr(user, field, validated_data['admin'][field])
        user.save()
        
        
            
        return 

    

   
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)



    