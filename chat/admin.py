from django.contrib import admin
from .models import Conversation, Message

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_conversation', 'receiver_conversation', 'start_time')
    list_filter = ('start_time',)
    search_fields = ('sender_conversation__username', 'receiver_conversation__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'text', 'attachment', 'conversation_id', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'text', 'conversation_id__id')

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)