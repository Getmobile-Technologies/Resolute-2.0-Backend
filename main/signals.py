from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import PanicRequest, EmergencyContact, CallRequest
from accounts.helpers.sms import emergency_sms, call_emergency_sms
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

User = get_user_model()



@receiver(post_save, sender=PanicRequest)
def send_emergency_sms(instance, created, **kwargs):
    if created:
        contacts = list(EmergencyContact.objects.filter(is_deleted=False).values_list('phone'))
        admin = instance.user.user
        contacts.append(admin.phone)
        for contact in contacts:
            emergency_sms(
                panic=instance,
                phone=contact
            )

        return 
    


@receiver(post_save, sender=CallRequest)
def call__emergency_sms(instance, created, **kwargs):
    if created:
        contacts = list(EmergencyContact.objects.filter(is_deleted=False).values_list('phone'))
        admin = instance.user.user
        contacts.append(admin.phone)
        for contact in contacts:
            call_emergency_sms(
                panic=instance,
                phone=contact
            )

        return




# @receiver(post_save, sender=Notifications)
# def send_notification(sender, instance:Notifications, created, *args,**kwargs):
    
#     if created:        
#         if instance.organisation.contact_admin.fcm_token:
        
#             notification = messaging.Notification(title="New notiffication", body=instance.message)
#             messaging.send(messaging.Message(notification=notification, token=instance.organisation.contact_admin.fcm_token))
#     return
