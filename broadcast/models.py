from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.

class LocationData(models.Model):
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    staff =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
    
    
    