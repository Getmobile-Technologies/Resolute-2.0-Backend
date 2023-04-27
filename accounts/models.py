from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import UserManager
from django.core.validators import RegexValidator
from django.db.models import Count
from django.db.models import Q



class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")

    first_name = models.CharField(_('first_name'), max_length=250)
    last_name = models.CharField(_('last_name'), max_length=250)
    phone = models.CharField(_('phone'), max_length=200, unique=True, null=True)#remember to use phone regex for production
    email = models.EmailField(_('email'), unique=True, null=True, blank=True)
    location = models.CharField(_('location'), max_length=300, null=True)
    role = models.CharField(_('role'), max_length=100, null=True)
    password = models.CharField(_('password'), max_length=100, null=True, blank=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    user = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="mapped_users")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'email']

    objects = UserManager()


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone

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



    # def delete(self):
    #     self.is_deleted = True
    #     self.email = f"{random.randint}-deleted-{self.email}"
    #     self.phone = f"{self.phone}-deleted-{random.randint}"
    #     self.save()


