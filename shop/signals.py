from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


