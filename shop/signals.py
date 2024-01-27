from time import sleep

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Customer, Order, Transaction, OrderItem


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=Order)
def create_transaction_for_new_order(sender, instance: Order, created, **kwargs):
    order = instance
    if created:
        sleep(0.5)
        total_price = order.get_total_price()
        print(total_price)
        customer = instance.customer
        receipt_number = None
        Transaction.objects.create(order=order, customer=customer, total_price=total_price,
                                   receipt_number=receipt_number)
    else:
        transaction = Transaction.objects.get(order=order)
        total_price = order.get_total_price()
        transaction.total_price = total_price
        transaction.save()


@receiver(post_save, sender=OrderItem)
def update_total_sales_of_transaciton(sender, instance, created, **kwargs):
    order_item: OrderItem = instance
    order = order_item.order
    transaction = Transaction.objects.get(order=order)
    total_price = order.get_total_price()
    transaction.total_price = total_price
    transaction.save()
