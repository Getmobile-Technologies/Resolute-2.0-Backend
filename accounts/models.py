from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import UserManager
from django.core.validators import RegexValidator




class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")

    first_name = models.CharField(_('first_name'), max_length=250)
    last_name = models.CharField(_('last_name'), max_length=250)
    phone = models.CharField(_('phone'), max_length=200, unique=True, null=True)
    email = models.EmailField(_('email'), unique=True, null=True, blank=True)
    location = models.CharField(_('location'), max_length=200, null=True)
    role = models.CharField(_('role'), max_length=100, null=True)
    password = models.CharField(_('password'), max_length=100, null=True, blank=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
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

