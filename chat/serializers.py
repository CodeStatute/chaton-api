from rest_framework import serializers
from user.models import User
from .models import Chat


class FindConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GetChatRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
