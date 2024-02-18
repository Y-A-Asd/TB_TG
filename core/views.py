# views.py
import json
import logging
import redis
import requests
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.views import UserViewSet as BaseUserViewSet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import SendRequestSerializer
from .models import User
from .otp import Authentication
from django.conf import settings
import subprocess

security_logger = logging.getLogger('security_logger')


class UserCreateView(BaseUserViewSet, APIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
            return Response({'message': _('You already registered!')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except User.DoesNotExist:
            user = User(**serializer.validated_data)
        user.save()
        security_logger.info(f'new user created with phone_number {serializer.validated_data["phone_number"]}')
        return Response({'message': _('Account created !')}, status=status.HTTP_201_CREATED)


class UserLoginOTPView(APIView):
    """
    {
    "email": "user@user.user",
    }
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        security_logger.info(f'user with email {email} wants to log in with code')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': _('Invalid Email')}, status=status.HTTP_400_BAD_REQUEST)

        otp_key = f'otp:{user.email}'
        redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        otp_is_send = redis_connection.get(otp_key)
        if otp_is_send:
            return Response({'error': _('Wait until last code expire')}, status=status.HTTP_201_CREATED)
        try:
            otp, otp_expiry = Authentication.send_otp_email(user.email, otp_key)
            security_logger.info(f'send code for user {email} : {otp}')
            return Response({'message': _('Code Send, Check you email')}, status=status.HTTP_201_CREATED)
        except ConnectionError:
            security_logger.info(f'server can not send email!')
            return Response({'error': _('server side error!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        security_logger.info(f'user {email} entered code: {entered_otp} -> actual code: {stored_otp}')
        if str(stored_otp.decode('utf_8')) == str(entered_otp):
            user = get_user_model().objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            security_logger.info(f'user {email} login with code!')
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': _('Invalid Code')}, status=status.HTTP_400_BAD_REQUEST)


class ZarinpalRequestView(APIView):
    """
    {
        "phone_number": "09353220545",
        "total_price": "10000",
    }
    """
    serializer_class = SendRequestSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        total_price = request.data.get('total_price', '')
        description = f'user {phone_number} wants to pay {total_price}'
        MERCHANT = settings.MERCHANT
        ZP_API_REQUEST = settings.ZP_API_REQUEST
        ZP_API_STARTPAY = settings.ZP_API_STARTPAY
        CallbackURL = 'http://yoursite.com/verify'

        try:
            curl_command = [
                'curl',
                '-X', 'POST', f'{ZP_API_REQUEST}',
                '-H', 'accept: application/json',
                '-H', 'content-type: application/json',
                '-d',
                json.dumps({
                    'merchant_id': MERCHANT,
                    'amount': int(total_price),
                    'callback_url': CallbackURL,
                    'description': description
                })
            ]
            print(curl_command)
            try:
                result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                    try:
                        json_response = json.loads(result.stdout)
                        print(json_response)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON response: {e}")
                else:
                    print(f"Error executing curl command. Error message:\n{result.stderr}")
            except FileNotFoundError:
                print("Curl executable not found. Make sure curl is installed.")

        #     if response.status_code == 200:
        #         print('status 200')
        #         response = response.json()
        #         if response['Status'] == 100:
        #             print('status 100')
        #             return Response({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
        #                              'authority': response['Authority']})
        #         else:
        #             return Response({'status': False, 'code': str(response['Status'])})
        #     return Response({'status': False, 'code': str(response.status_code)})
        #
        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ZarinpalVerifyView(APIView):
    """
    {
        "Authority": "######",
        "total_price": "10000",
    }
    """
    serializer_class = SendRequestSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ZP_API_VERIFY = settings.ZP_API_VERIFY
        Authority = request.data.get('Authority', '')
        total_price = request.data.get('total_price', '')
        MERCHANT = settings.MERCHANT

        data = {
            "MerchantID": MERCHANT,
            "Amount": total_price,
            "Authority": Authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return Response({'status': True, 'RefID': response['RefID']})
            else:
                return Response({'status': False, 'code': str(response['Status'])})
        return Response({'status': False, 'code': str(response.status_code)})
