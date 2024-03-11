import base64
import json
import secrets
import time
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from jwt import decode, InvalidTokenError
from core.models import User
from core.models import User
from .models import Message, Conversation
from .serializers import MessageSerializer

SECRET_KEY = '0uwk9*8mltebnrrdn(zawxdyh-8b*s6$!0n(lb(cwlk+@otvzq' #todo


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("here")
        print(self.scope)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        time.sleep(2)
        # Send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):

        text_data_json = event.copy()
        text_data_json.pop("type")
        message, attachment, header = (
            text_data_json["message"],
            text_data_json.get("attachment"),
            text_data_json.get("headers"),
        )
        print('self.room_name', self.room_name)
        conversation = Conversation.objects.get(id=int(self.room_name))
        if header:
            token = header['Authorization'].split()[1]
            print(token)
            print(type(token))
            decoded_token = decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            user = User.objects.get(id=user_id)
            sender = user
        else:
            sender = self.scope['user']

        print(self.scope)
        print()
        print(self.scope)
        print()
        print()
        print('text_data_json', text_data_json)
        try:
            if sender:
                # Attachment
                if attachment:
                    file_str, file_ext = attachment["data"], attachment["format"]

                    file_data = ContentFile(
                        base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
                    )
                    _message = Message.objects.create(
                        sender=sender,
                        attachment=file_data,
                        text=message,
                        conversation_id=conversation,
                    )
                else:
                    _message = Message.objects.create(
                        sender=sender,
                        text=message,
                        conversation_id=conversation,
                    )
                serializer = MessageSerializer(instance=_message)
                # Send message to WebSocket
                self.send(
                    text_data=json.dumps(
                        serializer.data
                    )
                )
            else:
                raise ValueError('Sender is not found Log in please')
        except Exception as e:
            error_message = {"error": str(e)}
            self.send_error(error_message)

    def send_error(self, error_message):
        # Send error message to WebSocket
        self.send(text_data=json.dumps(error_message))
