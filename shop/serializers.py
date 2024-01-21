from decimal import Decimal

from rest_framework import serializers

from shop.models import Product, Collection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'price', 'price_with_tax', 'collection']

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    """4 ways to serialize relations : 1.pk 2.object 3.string 4.hyperlink"""

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    """validation example"""
    # def validate(self,data):
    #     if True:
    #         return data
    #     else: return serializers.ValidationError('msg')

    """create method overwrite"""
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    """update method overwrite"""
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'parent', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
