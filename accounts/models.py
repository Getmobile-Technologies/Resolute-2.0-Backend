from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import uuid
import re
from .managers import UserManager
from django.core.validators import RegexValidator
from django.db.models import Count
from django.utils import timezone
import random
from django.db.models import Q
from django.forms import model_to_dict



class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")

    first_name = models.CharField(_('first_name'), max_length=250)
    last_name = models.CharField(_('last_name'), max_length=250)
    phone = models.CharField(_('phone'), max_length=200, null=True, validators=[phone_regex])
    email = models.EmailField(_('email'), unique=True, null=True, blank=False)
    location = models.ForeignKey("main.StaffLocation", on_delete=models.CASCADE, null=True)
    organisation = models.ForeignKey("accounts.Organisations", on_delete=models.CASCADE, null=True)
    role = models.CharField(_('role'), max_length=100, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    fcm_token = models.TextField(null=True)
    user = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="mapped_users")
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'email']

    objects = UserManager()


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone
        
    def delete(self):
        self.is_deleted=True
        self.is_active=False
        self.phone = self.phone + f"--deleted--{timezone.now()}"
        self.email = f"deleted--{timezone.now()}" + self.email if self.email else f"deleted--{timezone.now()}@--no-email-added.com"
        self.save()
        
        if self.role == "staff":
            
            #Delete corresponding data
            
            self.user_request.filter(is_deleted=True).update(is_deleted=True)
            self.capture_request.filter(is_deleted=True).update(is_deleted=True)
            self.call_request.filter(is_deleted=True).update(is_deleted=True)
            self.track_request.filter(is_deleted=True).update(is_deleted=True)


        

  
    
    @property
    def total_admin_panic(self):
        user_requests_count = self.mapped_users.annotate(user_request_count=Count('user_request'))
        total_user_requests_count = sum(mapped_user.user_request_count for mapped_user in user_requests_count)
        return total_user_requests_count

    @property
    def total_reviewed_panic(self):
        user_requests_count = self.mapped_users.annotate(user_reviewed_request_count=Count('user_request', filter=Q(user_request__is_reviewed=True)))
        total_user_reviewed_requests_count = sum(mapped_user.user_reviewed_request_count for mapped_user in user_requests_count)
        return total_user_reviewed_requests_count
    
    @property
    def total_unreviewed_panic(self):
        user_requests_count = self.mapped_users.annotate(user_reviewed_request_count=Count('user_request', filter=Q(user_request__is_reviewed=False)))
        total_user_reviewed_requests_count = sum(mapped_user.user_reviewed_request_count for mapped_user in user_requests_count)
        return total_user_reviewed_requests_count

    @property
    def total_ingenuine_panic(self):
        user_requests_count = self.mapped_users.annotate(user_genuine_request_count=Count('user_request', filter=Q(user_request__is_genuine=False)))
        total_user_genuine_requests_count = sum(mapped_user.user_genuine_request_count for mapped_user in user_requests_count)
        return total_user_genuine_requests_count


    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id","name"])
    
    @property
    def location_data(self):
        return model_to_dict(self.location, fields=["id", "city", "state"])


    @property
    def contact_admin_data(self):
        return model_to_dict(self.organisation.contact_admin, fields=["id","first_name", "last_name", "email"])


class Organisations(models.Model):
    name = models.CharField(max_length=250, null=True, unique=True)
    category = models.ForeignKey("main.Category", on_delete=models.CASCADE)
    contact_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_users")
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_deleted=True
        self.save()
        #TODO: get all the corresponding users, admins and soft delete their accounts -- FEMI!
        
    @property
    def admin_data(self):
        return model_to_dict(self.contact_admin)
    
    @property
    def category_data(self):
        return model_to_dict(self.category)
    
    @property
    def total_registered_users(self):
        return self.user_set.filter(role="staff", is_deleted=False).count()
    
    @property
    def total_incidence(self):
        return self.panicrequest_set.filter(is_deleted=False).count()
    
    @property
    def resolved_incidence(self):
        return self.panicrequest_set.filter(is_deleted=False, is_reviewed=True).count()
    
    @property
    def unresolved_incidence(self):
        return self.panicrequest_set.filter(is_deleted=False, is_reviewed=False).count()
    
    @property
    def ingenuine_incidence(self):
        return self.panicrequest_set.filter(is_deleted=False, is_genuine=False).count()
    
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="users_activity")
    organisation = models.CharField(max_length=250, null=True) #take this out
    timeline = models.CharField(max_length=300, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
