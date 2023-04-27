from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()



class PanicRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_request")
    longitude = models.CharField(max_length=200, null=True, blank=False)
    latitude = models.CharField(max_length=200, null=True, blank=False)
    location = models.CharField(max_length=200, null=True, blank=False)
    status = models.CharField(max_length=100, null=True, default='panic')
    is_reviewed = models.BooleanField(default=False)
    is_genuine = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)



class CallRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="call_request")
    phone = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, default='call_request')
    is_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class TrackMeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="track_request")
    longitude = models.CharField(max_length=200, null=True, blank=False)
    latitude = models.CharField(max_length=200, null=True, blank=False)
    location = models.CharField(max_length=200, null=True, blank=False)
    status = models.CharField(max_length=100, null=True, default='track_request')
    is_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="capture_request")
    image = models.ImageField(null=True, upload_to='capture')
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)




class StaffLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="staff_location")
    address = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=200, null=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.state