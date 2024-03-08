from django.shortcuts import render
from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import User
from .serializers import ConversationListSerializer, ConversationSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def start_conversation(request, ):
    """
    {
        "phone_number": "09353220545"
    }
    """
    data = request.data
    phone_number = data.pop('phone_number')
    try:
        participant = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    conversation = Conversation.objects.filter(Q(sender_conversation=request.user, receiver_conversation=participant) |
                                               Q(sender_conversation=participant, receiver_conversation=request.user))
    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(sender_conversation=request.user, receiver_conversation=participant)
        return Response(ConversationSerializer(sender_conversation=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(sender_conversation=request.user) |
                                                    Q(receiver_conversation=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
