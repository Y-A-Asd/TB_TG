from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import random
import os


class Authentication:

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp_email(to_email):
        otp = Authentication.generate_otp()

        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        subject = 'Your verification Code'
        message = f'Your code is: {otp}'

        try:

            email_from = 'djmailyosof@gmail.com'
            recipient_list = [to_email, ]
            send_mail(subject, message, email_from, recipient_list, auth_user=email_from,
                      auth_password=settings.EMAIL_HOST_PASSWORD)
            return otp, otp_expiry
        except Exception as e:
            return None

    # @staticmethod
    # def send_otp(phone_number):
    #     otp = Authentication.generate_otp()
    #     otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
    #
    #     account_sid = os.getenv('account_sid')
    #     auth_token = os.getenv('auth_token')
    #     twilio_phone_number = os.getenv('twilio_phone_number')
    #
    #     dist_phone_number = phone_number.replace("0", "+98", 1)
    #
    #     client = Client(account_sid, auth_token)
    #     # print("Phone Number:", dist_phone_number)
    #     message = client.messages.create(
    #         body=f'Your code is: {otp}',
    #         from_=twilio_phone_number,
    #         to=dist_phone_number
    #     )
    #
    #     # print("Twilio Response:", message)
    #     return otp, otp_expiry

    @staticmethod
    def check_otp(otp, otp_expiry, entered_otp):
        return otp == entered_otp and timezone.now() < otp_expiry
