from core.serializers import UserCreateSerializer
from .models import Conversation, Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    sender_conversation = UserCreateSerializer()
    receiver_conversation = UserCreateSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'sender_conversation', 'receiver_conversation', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        if message:
            serializer = MessageSerializer(instance=message)
            return serializer.data
        else:
            return None


class ConversationSerializer(serializers.ModelSerializer):
    sender_conversation = UserCreateSerializer()
    receiver_conversation = UserCreateSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['sender_conversation', 'receiver_conversation', 'message_set']
