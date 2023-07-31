import json
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import LocationData
from .serializers import LocationDataSerializer
from django.utils import timezone
import redis
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection

User = get_user_model()


class TrackMeConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.staff_id = self.scope['url_route']['kwargs']['id']
        self.track_id = self.scope['url_route']['kwargs']['track_id']

        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
        
        await self.accept()
        
        # Join user-specific group
        user_group_name = f'{self.staff_id}_tracking_{self.track_id}'
        await self.channel_layer.group_add(
            user_group_name,
            self.channel_name
        )
        
        # Check if Redis data storage already exists for the group
        redis_client = redis.Redis()
        storage_exists = await self.check_redis_storage(redis_client, user_group_name)
        
        print("Somebody joined", user_group_name)

        # If Redis data storage doesn't exist, create it and initialize the connection count
        if not storage_exists:
            await self.initialize_redis_storage(redis_client, user_group_name)
        else:
            await self.increment_connection_count(redis_client, user_group_name)
            await self.channel_layer.group_send(
            user_group_name,
            {
                'type': 'send_location',
                'location': {}
            }
        )

    async def disconnect(self, close_code):
        # Leave user-specific group
        user_group_name = f'{self.staff_id}_tracking_{self.track_id}'
        
        print("Somebody left", user_group_name)
        await self.channel_layer.group_discard(
            user_group_name,
            self.channel_name
        )
        
        # Decrement the connection count in Redis and delete the storage if count reaches zero
        redis_client = redis.Redis()
        await self.decrement_connection_count(redis_client, user_group_name)

    @database_sync_to_async
    def check_redis_storage(self, redis_client, user_group_name):
        return redis_client.exists(user_group_name)

    @database_sync_to_async
    def initialize_redis_storage(self, redis_client, user_group_name):
        redis_client.set(user_group_name, "")
        redis_client.set(f'{user_group_name}_connections', 1)

    @database_sync_to_async
    def increment_connection_count(self, redis_client, user_group_name):
        count_key = f'{user_group_name}_connections'
        count = redis_client.incr(count_key)
        print("Somebody joined", count)

    @database_sync_to_async
    def decrement_connection_count(self, redis_client, user_group_name):
        count_key = f'{user_group_name}_connections'
        count = redis_client.decr(count_key)
        print("Somebody left",count)
        # if count <= 0:
        #     redis_client.delete(user_group_name)
        #     redis_client.delete(count_key)
        

    async def receive(self, text_data):

        # location = json.loads(text_data)


        serializer = LocationDataSerializer(data=eval(text_data))
        serializer.is_valid(raise_exception=True)
        
        
        location = serializer.validated_data.copy()
        
        # Save location data asynchronously
        await self.save_location_data(serializer.validated_data, self.user)

    
        location['timestamp'] = timezone.now().isoformat()
        
        # Send location data to the recipient's group. Same channel
        recipient_group_name = f'{self.staff_id}_tracking_{self.track_id}'
        await self.channel_layer.group_send(
            recipient_group_name,
            {
                'type': 'send_location',
                'location': location
            }
        )
        
        # Append the location data to the communication history in Redis
        redis_client = redis.Redis()
        redis_client.append(recipient_group_name, json.dumps(location))
    

    async def send_location(self, event):
        location = event['location']

        # Retrieve the communication history from Redis
        redis_client = redis.Redis()
        user_group_name = f'{self.staff_id}_tracking_{self.track_id}'
        communication_history = redis_client.get(user_group_name)
        hist =communication_history.decode('utf-8')
        # Add commas between individual JSON objects to form a valid JSON array.
        formatted_history = "[" + hist.replace("}{", "},{") + "]"

        # Parse the JSON array into a list of dictionaries.
        data = json.loads(formatted_history)

        # Send message to WebSocket along with the communication history
        response = {
            'location': location,
            'communication_history': data
        }
        await self.send(text_data=json.dumps(response))
        
        
    @staticmethod
    @sync_to_async
    def save_location_data(data, user:User):
        print(LocationData.objects.all().count())
        if user.role == "staff":

            if LocationData.objects.exists():
                last_record = LocationData.objects.latest('id')
                timediff = (timezone.now() - last_record.timestamp).total_seconds()
                if timediff >= 5:
                    LocationData.objects.create(**data, staff=user)
            else:
                LocationData.objects.create(**data, staff=user)
