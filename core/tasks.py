# tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from TB_TG.settings.common import EMAIL_HOST_PASSWORD
from .models import User
from shop.models import Promotion, Cart

logger = get_task_logger(__name__)


@shared_task
def delete_inactive_users():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    inactive_users = get_user_model().objects.filter(created_at__lte=three_days_ago, is_active=False)
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
def delete_inactive_carts():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    inactive_carts = Cart.objects.filter(updated_at__lte=three_days_ago)

    for cart in inactive_carts:
        cart.delete()
        logger.info(f"Deleted inactive cart with ID {cart.id}.")
