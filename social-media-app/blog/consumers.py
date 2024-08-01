import json
from channels.generic.websocket import AsyncWebsocketConsumer
from blog.models import ChatMessage
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
