from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()
# Create your models here.



class PanicRequest(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_request")
    status = models.CharField(max_length=100, null=True, default='panic')
    IsReviewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)



class CallRequest(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="call_request")
    phone = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, default='call_request')
    isReviewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
