from django.db import models
import uuid

import random


# ! handle all the chats
class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, auto_created=True)
    text_message = models.TextField()
    chat_room_id = models.BigIntegerField() 
    user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
