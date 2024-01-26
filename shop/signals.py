from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Customer, Order, Transaction


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=Order)
def create_transaction_for_new_order(sender, instance: Order, created, **kwargs):
    # if created :
    total_price = instance.get_total_price()
    order = instance
    customer = instance.customer
    receipt_number = None
    Transaction.objects.create(order=order, customer=customer, total_price=total_price, receipt_number=receipt_number)
