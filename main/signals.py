from django.dispatch import receiver
from django.db.models.signals import post_save
from . models import PanicRequest, EmergencyContact
from accounts.helpers.sms import emergency_sms






@receiver(post_save, sender=PanicRequest)
def send_emergency_sms(instance, created, **kwargs):
    if created:
        contacts = EmergencyContact.objects.filter(is_deleted=False)
        for contact in contacts:
            emergency_sms(
                panic=instance,
                phone=contact.phone
            )

    return 




