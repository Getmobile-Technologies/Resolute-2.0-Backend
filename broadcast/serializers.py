from rest_framework import serializers
from .models import LocationData

class LocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LocationData
        fields = "__all__"
        
        