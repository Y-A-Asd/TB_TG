# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from djoser.views import UserViewSet as BaseUserViewSet
from djoser.views import TokenCreateView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .otp import Authentication
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
import redis


class UserCreateView(BaseUserViewSet, APIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(dict(serializer.validated_data))
        try:
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
        except User.DoesNotExist:
            user = User.objects.create_user(**serializer.validated_data)

        otp_key = f'otp:{user.email}'
        print(user.email)
        otp, otp_expiry = Authentication.send_otp_email(user.email, otp_key)
        print('here')

        return Response({'otp_expiry': otp_expiry}, status=status.HTTP_201_CREATED)


class VerifyOtpView(APIView):
    """
    {
    "email": "user@user.user",
    "otp": "111111"
    }
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        entered_otp = request.data.get('otp', '')

        otp_key = f'otp:{email}'
        print(otp_key)
        stored_otp = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB).get(otp_key)
        print(stored_otp, entered_otp, stored_otp.decode('utf-8'))
        if stored_otp and stored_otp.decode('utf-8') == entered_otp:
            user = get_user_model().objects.get(email=email)
            user.is_active = True
            user.save()

            return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
