from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import Chat
from .serializers import GetChatRoomMessageSerializer
from datetime import datetime


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.chat_room_id = str(
            self.scope["url_route"]["kwargs"]["chat_room_id"]
        )

        self.user_id = str(
            self.scope["url_route"]["kwargs"]["user_id"]
        )

        await self.channel_layer.group_add(
            self.chat_room_id,
            self.channel_name
        )

        print("ws connected...")

    async def receive_json(self, content, **kwargs):
        await database_sync_to_async(Chat.objects.create)(
            chat_room_id=self.chat_room_id,
            user_id=self.user_id,
            text_message=content["message"],
        )

        record = Chat(
            chat_room_id=self.chat_room_id,
            user_id=self.user_id,
            text_message=content["message"],
            created_at=datetime.now()
        )

        data = GetChatRoomMessageSerializer(record).data

        await self.channel_layer.group_send(
            self.chat_room_id,
            {
                "type": "chat.message",
                "text": data
            }
        )

    async def chat_message(self, event):
        await self.send_json({"message": event["text"]})

    async def disconnect(self, close_code):
        print("ws disconnected...", close_code)
        raise StopConsumer()
