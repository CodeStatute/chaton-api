from django.urls import path
from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    path("ws/chat-room/<int:chat_room_id>/<uuid:user_id>/",
         ChatRoomConsumer.as_asgi(), name="chat_consumer")
]
