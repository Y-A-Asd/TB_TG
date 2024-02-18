from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework.serializers import ModelSerializer

from shop.models import Transaction


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'phone_number', 'email', 'password']


class SendRequestSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['phone_number', 'total_price']


class VerifySerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['total_price', 'Authority']
