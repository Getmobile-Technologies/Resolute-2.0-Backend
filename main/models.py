from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from accounts.models import Organisations
from django.forms import model_to_dict

User = get_user_model()



class PanicRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_request")
    longitude = models.CharField(max_length=200, null=True, blank=False)
    latitude = models.CharField(max_length=200, null=True, blank=False)
    location = models.CharField(max_length=200, null=True, blank=False)
    user_location = models.CharField(max_length=300, null=True, blank=True) #location assigned to a user upon create
    status = models.CharField(max_length=100, null=True, default='panic')
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    is_reviewed = models.BooleanField(default=False)
    is_genuine = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()

    @property
    def user_data(self):
        return model_to_dict(self.user, fields=["first_name", "last_name", "email", "phone"]) if self.user.is_deleted == False else {}
    
    
    @property
    def location_data(self):
        return model_to_dict(self.user.location, fields=["city", "state"])
    
    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])
    



class CallRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="call_request")
    phone = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, default='call_request')
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    is_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()
    

    @property
    def user_data(self):
        return model_to_dict(self.user, fields=["first_name", "last_name", "email", "phone"]) if self.user.is_deleted == False else {}
    
    
    @property
    def location_data(self):
        return model_to_dict(self.user.location, fields=["city", "state"])
    
    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])


class TrackMeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="track_request")
    longitude = models.CharField(max_length=200, null=True, blank=False)
    latitude = models.CharField(max_length=200, null=True, blank=False)
    location = models.CharField(max_length=200, null=True, blank=False)
    organisation = models.ForeignKey("accounts.Organisations", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True, default='track_request')
    is_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()


    @property
    def user_data(self):
        return model_to_dict(self.user, fields=["first_name", "last_name", "email", "phone"]) if self.user.is_deleted == False else {}
    

    @property
    def location_data(self):
        return model_to_dict(self.user.location, fields=["city", "state"])
    
    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])



class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="capture_request")
    image = models.ImageField(null=True, upload_to='capture')
    location = models.CharField(max_length=300, null=True, blank=False)
    organisation = models.ForeignKey("accounts.Organisations", on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()

    @property
    def user_data(self):
        return model_to_dict(self.user, fields=["first_name", "last_name", "email", "phone"]) if self.user.is_deleted == False else {}
    
    @property
    def location_data(self):
        return model_to_dict(self.user.location, fields=["city", "state"])
    
    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])




class StaffLocation(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=250, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.state
        

    def delete(self):
        self.is_deleted=True
        self.save()

    
    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])

class Notifications(models.Model):
    message = models.CharField(max_length=300, null=True)
    organisation = models.ForeignKey("accounts.Organisations", on_delete=models.CASCADE, related_name="organisation_notifications")
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()

    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_deleted=True
        self.save()


class EmergencyContact(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")

    full_name = models.CharField(max_length=350, null=True, blank=True)
    phone = models.CharField(max_length=200, unique=True, null=True, validators=[phone_regex], blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=False)


    def delete(self):
        self.is_deleted=True
        self.phone = self.phone + f"--deleted--{timezone.now()}"
        self.save()
