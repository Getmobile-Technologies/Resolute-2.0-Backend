from django.dispatch import receiver
from django.db.models.signals import post_save
from . models import PanicRequest, EmergencyContact
from accounts.helpers.sms import emergency_sms
import random
from accounts.models import Organisations 
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from djoser.signals import user_registered, user_activated
from django.utils import timezone
from main.models import Notifications
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import os
import  requests
from firebase_admin import messaging





@receiver(post_save, sender=PanicRequest)
def send_emergency_sms(instance, created, **kwargs):
    if created:
        contacts = EmergencyContact.objects.filter(is_deleted=False)
        admin = Organisations.objects.filter(name=instance.organisation)
        phone = admin.user.phone
        # contacts.append(admin_phone)
        # for contact in contacts:
        emergency_sms(
            panic=instance,
            phone=phone
        )

    return 




@receiver(post_save, sender=Notifications)

def send_notification(sender, instance:Notifications, created, *args,**kwargs):
    
    if created:        
        if instance.user.fcm_token:
        
            notification = messaging.Notification(title=instance.heading, body=instance.body, image=instance.image_url)
            messaging.send(messaging.Message(notification=notification, token=instance.user.fcm_token))
    return
