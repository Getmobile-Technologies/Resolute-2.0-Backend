from django.urls import path
from .consumers import TrackMeConsumer

websocket_urlpatterns = [
    path('ws/<str:track_id>/tracker/<str:id>/', TrackMeConsumer.as_asgi()),

]