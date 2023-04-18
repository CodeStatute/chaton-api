from django.urls import path
from .controllers.connection import FindConnectionApiView,  MakeNewConnectionApiView, GetChatConnectionsApiView, GetChatRoomMessages


urlpatterns = [
    path('find-connection/',
         FindConnectionApiView.as_view(), name='find_connection'),

    path('make-connection/',
         MakeNewConnectionApiView.as_view(), name='make_connection'),

    path('get-chat-connections/',
         GetChatConnectionsApiView.as_view(), name='get_chat_connections'),

    path('get-chat-room-messsages/',
         GetChatRoomMessages.as_view(), name='get_chat_room_messages'),
]
