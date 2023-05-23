from rest_framework import serializers
from .models import PanicRequest, CallRequest, TrackMeRequest, StaffLocation, Images, Notifications, Category, EmergencyContact









class PanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanicRequest
        fields = '__all__'



class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRequest
        fields = '__all__'



class TrackMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackMeRequest
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffLocation
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class CatgorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class FirebaseSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=6000)