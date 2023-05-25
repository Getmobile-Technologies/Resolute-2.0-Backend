from django.contrib import admin
from .models import PanicRequest, CallRequest, TrackMeRequest, StaffLocation, Images, Notifications, EmergencyContact

# Register your models here.


admin.site.register([
    PanicRequest,
    CallRequest,
    TrackMeRequest,
    StaffLocation,
    Images,
    Notifications,
    EmergencyContact
])

