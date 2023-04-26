from rest_framework import serializers
from .models import PanicRequest, CallRequest, TrackMeRequest, StaffLocation









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