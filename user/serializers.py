from rest_framework import serializers
from .models import User, UserRelation


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username",
                  "email", "profile", "connection_id"]


class UserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelation
        fields = "__all__"
        read_only_fields = ['chat_room_id', 'created_at']
        extra_kwargs = {
            'from_user': {'write_only': True},
            'to_user': {'write_only': True},
        }
