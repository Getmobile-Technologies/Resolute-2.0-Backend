"""
ASGI config for res_config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'res_config.settings')
django.setup()

application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from broadcast.routing import websocket_urlpatterns
from broadcast.middlewares import JWTTokenAuthMiddleware


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTTokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})