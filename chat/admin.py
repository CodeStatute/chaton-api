from django.contrib import admin

# Register your models here.
from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["text_message", "chat_room_id", "created_at"]
