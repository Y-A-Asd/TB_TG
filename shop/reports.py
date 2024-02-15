from collections import namedtuple
from datetime import timedelta
from decimal import Decimal

from django.db.models import Q, Func, ExpressionWrapper, Sum, DecimalField, F, Count
from django.db.models.functions import ExtractHour
from django.utils import timezone

from .models import Order, Product, OrderItem, Collection


class Reporting:
    """
    Total sales              *
    favorite tables          *
    favorite foods           *
    generate Sales Invoice
    """

    def __init__(self, kwargs):
        # print(kwargs)
        if 'days' in kwargs:
            # print('here')
            self.days = kwargs['days']
            self.time_filter = Q(created_at__gte=timezone.now() - timezone.timedelta(days=self.days))
        elif 'start_at' in kwargs and 'end_at' in kwargs:
            # print('here too')
            self.start_at = kwargs['start_at']
            self.end_at = kwargs['end_at'] + timedelta(days=1)
            self.time_filter = Q(created_at__range=[self.start_at, self.end_at])

    def total_sales(self):
        """
        By using ExpressionWrapper in combination with annotate or other queryset methods,
         you can include more complex database expressions in your queries,
          providing flexibility and allowing you to perform calculations directly at the database level.
        """
        # def total_sales(self):
        #     orders = Order.objects.filter(
        #         created_at__gte=timezone.now()
        #                         - timezone.timedelta(days=self.days),status__in=["F"])
        #
        #     total_sales = orders.aggregate(
        #         total_sales=Sum(F('items__unit_price_after_off') * F('items__quantity'))
        #     )
        #     return total_sales['total_sales']

        orders = Order.objects.filter(
            self.time_filter,
            order_status__in=['P', 'S', 'D']
        )

        class RoundDecimal(Func):
            """
                https://stackoverflow.com/questions/17085898/conversion-of-datetime-field-to-string-in-django-queryset-values-list
                https://docs.djangoproject.com/en/1.8/ref/models/expressions/
            """
            function = 'ROUND'
            template = '%(function)s(%(expressions)s, 2)'

        # total_sales = orders.aggregate(
        #     total_sales=ExpressionWrapper(Round(Sum(
        #         F('items__unit_price') * F('items__quantity') -
        #         (F('items__unit_price') * F('items__quantity') * F('discount') / Decimal(100.0)),
        #         output_field=DecimalField(max_digits=10, decimal_places=2)
        #     ), output_field=DecimalField(max_digits=10, decimal_places=2),precision=2
        #     ), output_field=DecimalField(max_digits=10, decimal_places=2)
        #     )
        # ) or Decimal('0.00')

        total_sales = orders.aggregate(
            total_sales=ExpressionWrapper(
                RoundDecimal(
                    Sum(
                        RoundDecimal(F('orders__unit_price') * 1.0000000001 * F('orders__quantity')) -
                        RoundDecimal(
                            F('orders__unit_price') * 1.0000000001 * F('orders__quantity')),
                        output_field=DecimalField(max_digits=10, decimal_places=4)
                    )
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ) or Decimal('0.00')

        """
        https://www.reddit.com/r/djangolearning/comments/jtvbxn/rounding_an_aggregation_to_2_decimal_places/
        https://docs.djangoproject.com/en/5.0/ref/models/expressions/#using-f-with-annotations
        https://docs.djangoproject.com/en/5.0/ref/models/querysets/#sum
        https://stackoverflow.com/questions/69298226/how-can-i-round-an-sum-in-django-ojbect
        """
        # if total_sales['total_sales'] :
        #     pass
        # else:
        #     total_sales['total_sales'] =0
        return total_sales['total_sales']

    def favorite_products(self):
        """
        collections.namedtuple is a factory function in Python's collections module that creates
         a new class with named fields. It returns a new class type that can be used to create tuples
          with named fields.
        used namedtuple to create a simple data structure (ProductData) to represent
         the data for each food item with named fields. This makes it easier to manage and access
          the attributes in the template.
        """
        ProductData = namedtuple('ProductData', ['id', 'name', 'total_sales', 'counts', 'collection'])

        try:
            time_filter = Q(orderitems__order__created_at__gte=timezone.now()
                                                               - timezone.timedelta(days=self.days))
        except AttributeError:
            time_filter = Q(orderitems__order__created_at__range=[self.start_at, self.end_at])

        most_used_products = (
            Product.objects
            .filter(
                time_filter,
                orderitems__order__order_status__in=['P', 'S', 'D']
            )
            .annotate(
                used_products=Sum('orderitems__quantity', distinct=True),
                total_sales=Sum(
                    (F('orderitems__unit_price') * 1.0000000001 * F('orderitems__quantity'))
                    , output_field=DecimalField()
                )

            )
            .select_related('collection')
            .order_by('-used_products')
        )

        print(OrderItem._meta.get_field('unit_price').get_internal_type())
        print(OrderItem._meta.get_field('quantity').get_internal_type())

        for product in most_used_products:
            if product.used_products > 0:
                product_data = ProductData(
                    id=product.pk,
                    name=product.title,
                    total_sales=round(product.total_sales, 2),
                    counts=product.used_products,
                    collection=product.collection.title,
                )
                yield product_data

    def best_cutomer(self):
        orders = Order.objects.filter(
            self.time_filter,
            order_status__in=['P', 'S', 'D']
        )
        best_customer_data = (
            orders
            .values('customer__first_name', 'customer__last_name', 'customer__user__phone_number')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )
        if best_customer_data:
            return list(best_customer_data[0].values())
        else:
            return 'No user found'

    def favorite_collection(self):
        CollectionData = namedtuple('CollectionData', ['id', 'name', 'total_sales'])

        try:
            time_filter = Q(products__orderitems__order__created_at__gte=timezone.now()
                                                                         - timezone.timedelta(days=self.days))
        except AttributeError:
            time_filter = Q(products__orderitems__order__created_at__range=[self.start_at, self.end_at])

        most_used_categories = (
            Collection.objects
            .filter(
                time_filter,
                products__orderitems__order__order_status__in=['P', 'S', 'D']
            )
            .annotate(
                total_sales=Sum(
                    F('products__orderitems__quantity') * 1.0000000001 * F('products__orderitems__unit_price')
                    , output_field=DecimalField()
                )
            )
            .order_by('-total_sales')
        )

        for collection in most_used_categories:
            if collection.total_sales > 0:
                collection_data = CollectionData(
                    id=collection.pk,
                    name=collection.title,
                    total_sales=collection.total_sales,
                )
                yield collection_data

    def order_status_counts(self):

        OrderStatusCount = namedtuple('OrderStatusCount', ['status', 'count'])

        status_counts = (
            Order.objects
            .values('order_status').filter(self.time_filter)
            .annotate(count=Count('id'))
            .order_by('order_status')
        )

        result_data = [
            OrderStatusCount(
                status=status_data['order_status'],
                count=status_data['count']
            )
            for status_data in status_counts
        ]

        # print(result_data)
        return result_data
