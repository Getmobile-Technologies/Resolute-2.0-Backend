from django.dispatch import receiver
from django.db.models.signals import post_save
from . models import PanicRequest, EmergencyContact
from accounts.helpers.sms import emergency_sms






@receiver(post_save, sender=PanicRequest)
def send_emergency_sms(sender, instance, created, **kwargs):
    if created:
        try:
            contacts = EmergencyContact.objects.all()
        except EmergencyContact.DoesNotExist:
            print("fail")
            return
        for contact in contacts:
            emergency_sms(
                location=instance.location,
                long=instance.longitude,
                lat=instance.latitude,
                emergency_con=contact.phone
            )
        print("check")

        return




