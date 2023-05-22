import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
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



# def send_notification(sender, instance:Notifications, created, *args,**kwargs):
    
#     if created:        
#         if instance.user.fcm_token:
        
#             notification = messaging.Notification(title=instance.heading, body=instance.body, image=instance.image_url)
#             messaging.send(messaging.Message(notification=notification, token=instance.user.fcm_token))
#     return




# @receiver(post_save, sender=P)