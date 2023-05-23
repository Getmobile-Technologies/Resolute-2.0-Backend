from main.models import Notifications

def notification_handler(organisation, status):
    Notifications.objects.create(organisation=organisation, status=status)

    return 