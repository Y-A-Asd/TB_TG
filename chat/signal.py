from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


@receiver(post_save, sender=Message)
def delete_even_id_message(sender, instance, created, **kwargs):
    if created and instance.id % 2 == 0:
        instance.delete()
