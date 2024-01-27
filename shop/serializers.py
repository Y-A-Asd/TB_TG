from decimal import Decimal
from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers
from shop.models import Product, Collection, Review, Customer, Order, OrderItem, ProductImage, CartItem, Cart
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from django.utils.translation import gettext_lazy as _


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)

    class Meta:
        model = Product
        fields = ['id', 'translations', 'description', 'inventory',
                  'price', 'price_with_tax', 'collection_id', 'promotions', 'images']

    images = ProductImageSerializer(many=True, read_only=True)
    collection_id = serializers.IntegerField(required=False)
    price = serializers.DecimalField(max_digits=15, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    """4 ways to serialize relations : 1.pk 2.object 3.string 4.hyperlink"""

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    def create(self, validated_data):
        # Generate a slug based on the title
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update the slug if the title is modified
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)


class SimpleProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)

    class Meta:
        model = Product
        fields = ['id', 'translations', 'price']

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

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


class CollectionSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Collection)

    class Meta:
        model = Collection
        fields = ['id', 'translations', 'parent', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'created_at', 'parent_review', 'title', 'description', 'rating', 'user']

    def to_representation(self, instance):
        if instance.active:
            return super().to_representation(instance)
        return None

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price_after_off

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddItemsSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Prodcuts found!')
        else:
            return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Most be at least 1 !')
        else:
            return value


class UpdateItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Most be at least 1 !')
        else:
            return value


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'user_id', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'payment_status', 'orders']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No cart found!')
        if CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError('Cart is empty!')
        return value

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer, created = Customer.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
