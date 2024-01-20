from decimal import Decimal

from rest_framework import serializers

from shop.models import Product,Collection


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    """4 ways to serialize relations : 1.pk 2.object 3.string 4.hyperlink"""
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

