# tasks.py
import logging
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from TB_TG.settings.common import EMAIL_HOST_PASSWORD
from .otp import Authentication
from .models import User
from shop.models import Promotion, Cart, Customer

logger = get_task_logger(__name__)
security_logger = logging.getLogger('security_logger')


@shared_task
def send_otp_email_async(email, otp_key):
    try:
        otp, otp_expiry = Authentication.send_otp_email(email, otp_key)
        security_logger.info(f'Send code for user {email}: {otp}')
    except ConnectionError:
        security_logger.error('Server cannot send email!')


@shared_task
def delete_inactive_users():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    inactive_users = get_user_model().objects.filter(last_login__lte=three_days_ago, is_active=False)
    inactive_users.delete()
    logger.info(f"Deleted {inactive_users.count()} inactive users.")


@shared_task
def send_promotion_emails():
    one_days_ago = timezone.now() - timezone.timedelta(days=1)
    promotions = Promotion.objects.filter(created_at__gte=one_days_ago)

    for user in User.objects.all():
        subject = 'New Promotions!'
        message = 'Checkout our site to see all new promotions'
        to_email = user.email

        try:
            if promotions.exists():
                promotion_messages = "\n".join([f" - {promotion}" for promotion in promotions])
                message = f"New promotions available:\n{promotion_messages}\n\n{message}"
                send_mail(subject, message, 'djmailyosof@gmail.com', [to_email],
                          auth_user='djmailyosof@gmail.com', auth_password=EMAIL_HOST_PASSWORD)
                logger.info(f"Sent promotion email to {to_email}")
            else:
                logger.info(f"No new promotions to send to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send promotion email to {to_email}: {e}")


@shared_task
def send_birthday_emails():
    today = timezone.now().date()
    customers_with_birthdays = Customer.objects.filter(birth_date__month=today.month, birth_date__day=today.day)

    for customer in customers_with_birthdays:
        subject = 'Happy Birthday!'
        message = f"Dear {customer.first_name},\n\nHappy Birthday! We hope you have a fantastic day!"
        to_email = customer.user.email

        try:
            send_mail(subject, message, 'djmailyosof@gmail.com', [to_email],
                      auth_user='djmailyosof@gmail.com', auth_password=EMAIL_HOST_PASSWORD)
            logger.info(f"Sent birthday email to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send birthday email to {to_email}: {e}")


@shared_task
def delete_old_carts():
    five_days_ago = timezone.now() - timezone.timedelta(days=5)
    old_carts = Cart.objects.filter(updated_at__lte=five_days_ago)

    for cart in old_carts:
        cart.delete()
        logger.info(f"Deleted old cart with ID {cart.id}.")
