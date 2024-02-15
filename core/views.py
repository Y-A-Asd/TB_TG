# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from djoser.views import UserViewSet as BaseUserViewSet
from django.utils.translation import gettext_lazy as _
from .models import User
from .otp import Authentication
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
import redis


class UserCreateView(BaseUserViewSet, APIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(dict(serializer.validated_data))
        try:
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
        except User.DoesNotExist:
            user = User(**serializer.validated_data)

        otp_key = f'otp:{user.email}'
        redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        otp_is_send = redis_connection.get(otp_key)
        if otp_is_send:
            return Response({'error': _('Wait until last code expire')}, status=status.HTTP_201_CREATED)
        try:
            otp, otp_expiry = Authentication.send_otp_email(user.email, otp_key)
        except ConnectionError :
            return Response({'error': _('server side error!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # print('here')
        user.save()
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
        print(stored_otp, entered_otp)
        if str(stored_otp) == str(entered_otp):
            user = get_user_model().objects.get(email=email)
            user.is_active = True
            user.save()

            return Response({'message': _('User verified successfully')}, status=status.HTTP_200_OK)
        else:
            return Response({'message': _('Invalid Code')}, status=status.HTTP_400_BAD_REQUEST)
