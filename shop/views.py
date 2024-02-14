import logging
from django.db.models import Count, Q, QuerySet, ExpressionWrapper, fields, F
from django.utils.translation import gettext_lazy as _, activate, get_language
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from core.models import User, AuditLog
from discount.models import BaseDiscount
from .pagination import DefaultPagination
from .reports import Reporting
from .serializers import (ProductSerializer, CollectionSerializer, ReviewSerializer,
                          CartSerializer, CartItemSerializer, AddItemsSerializer, UpdateItemsSerializer,
                          CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer,
                          ProductImageSerializer, AddressSerializer, TransactionSerializer, UpdateTransactionSerializer,
                          AuditLogSerializer, PromotionSerializer, SimpleProductSerializer, ReportingSerializer,
                          SiteSettingsSerializer, HomeBannerSerializer, ApplyDiscountSerializer,
                          FeatureKeyFullSerializer)
from .models import Product, Collection, OrderItem, Review, Customer, Order, ProductImage, CartItem, Cart, Address, \
    Transaction, Promotion, SiteSettings, HomeBanner, MainFeature, FeatureKey
from .filters import ProductFilter, RecursiveDjangoFilterBackend, CustomerFilterBackend
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission

logger = logging.getLogger(__name__)
# logger.info()


# Create your views here.
"""class api view example"""
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def patch(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error' : 'can not be deleted!'})
#
"""function api view example"""
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products_count > 0:
#             return Response({'error': 'Collection cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""now we use GENERIC VIEW"""
"""https://www.django-rest-framework.org/api-guide/generic-views/"""

"""exasmple for overwriting these methods"""

# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.all().select_related('collection')
#
#     def get_serializer_class(self):
#         return ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
"""Generic view example"""
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'can not be deleted!'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'can not be deleted!'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""now we use View Set"""


class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [RecursiveDjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['translations__title', 'translations__description']
    ordering_fields = ['unit_price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    """we can manually filter by overwrite get_queryset function"""

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('images').prefetch_related('mainfeature_set')
        collection_id = self.request.query_params.get('collection_id')
        print('collection_id: ', collection_id)

        if collection_id:
            q_object = RecursiveDjangoFilterBackend().get_recursive_q(collection_id)
            queryset = queryset.filter(q_object)
        lt = self.request.query_params.get('unit_price__lt')
        gt = self.request.query_params.get('unit_price__gt')
        if lt and gt:
            unit_price_filters = RecursiveDjangoFilterBackend().get_unit_price_filters(self.request)
            queryset = queryset.filter(unit_price_filters)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(translations__title__contains=search)

        feature_key = self.request.query_params.get('feature_key')
        feature_value = self.request.query_params.get('feature_value')
        if feature_key:
            queryset = queryset.filter(mainfeature__key__id=feature_key)
        if feature_value:
            queryset = queryset.filter(mainfeature__value__id=feature_value)

        secondhand = self.request.query_params.get('secondhand')
        print('secondhand', secondhand)
        if secondhand == 'true':
            secondhand = True
            queryset = queryset.filter(secondhand=secondhand)
        if secondhand == 'false':
            secondhand = False
            queryset = queryset.filter(secondhand=secondhand)

        ordering = self.request.query_params.get('ordering', 'updated_at')
        queryset = queryset.order_by(ordering).distinct()

        return queryset

    def list(self, request, *args, **kwargs):
        logger.info("List view accessed")

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'can not be deleted!'})
        return super.destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).filter(parent__isnull=True)
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_products_count(self, collection):
        products_count = Product.objects.filter(collection=collection).count()
        subcollections = collection.subcollection.all()
        for subcollection in subcollections:
            products_count += self.get_products_count(subcollection)
        return products_count

    def update_products_count(self, data):
        for collection_data in data:
            collection = Collection.objects.get(id=collection_data['id'])
            collection_data['products_count'] = self.get_products_count(collection)
            if collection_data.get('children'):
                self.update_products_count(collection_data['children'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        self.update_products_count(data)

        return Response(data)

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection=kwargs['pk']).count() > 0:
            return Response({'error': 'can not be deleted!'})
        return super().destroy(request, *args, **kwargs)

    def filter_products_by_collection(self, collection):
        products = Product.objects.filter(collection=collection)
        subcollections = collection.subcollection.all()
        for subcollection in subcollections:
            products |= self.filter_products_by_collection(subcollection)
        return products

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        products = self.filter_products_by_collection(instance)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']
    serializer_class = ReviewSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    # pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        logger.info('test-logs')
        return Review.objects.filter(product_id=self.kwargs['product_pk'], active=True, parent_review=None)

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk'], 'user_id': self.request.user.id}

    @action(detail=True, methods=['GET'])
    def replies(self, request, *args, **kwargs):
        review = self.get_object()
        replies = Review.objects.filter(parent_review=review)
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')

        try:
            review = Review.objects.get(id=review_id, active=True)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(review)
        data = serializer.data

        replies = Review.objects.filter(parent_review=review)
        reply_serializer = self.get_serializer(replies, many=True)
        data['replies'] = reply_serializer.data

        return Response(data)


class PromotionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'PUT', 'POST']:
            return [IsAdminUser()]
        else:
            return []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        products = Product.objects.filter(promotions=instance)
        products_serializer = SimpleProductSerializer(products, many=True)
        data['products'] = products_serializer.data

        return Response(data)


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):

    def get_queryset(self):
        return Cart.objects.all().prefetch_related('items__product')

    serializer_class = CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            customer = Customer.objects.get(user_id=user_id)
            existing_cart = Cart.objects.filter(customer_id=customer.id).order_by('-updated_at').first()
            if existing_cart:
                serializer = self.get_serializer(existing_cart, data=request.data)
            else:
                serializer = self.get_serializer(data=request.data)
        except Customer.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get', 'post'])
    def apply_discount(self, request, pk=None):
        cart = self.get_object()

        if request.method == 'GET':
            serializer = ApplyDiscountSerializer()
            return Response(serializer.data)

        serializer = ApplyDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        discount_code = serializer.validated_data['discount_code']

        discount = get_object_or_404(BaseDiscount, code=discount_code)

        try:
            if not discount.ensure_availability():
                raise ValidationError(_("Discount is not available at the moment."))

            cart.discount = discount
            cart.save()

            return Response({'message': 'Discount applied successfully.'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddItemsSerializer
        elif self.request.method == 'PATCH':
            return UpdateItemsSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
    http_method_names = ['get', 'put']

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['membership', 'user_id']
    permission_classes = [IsAdminUser]

    """we can overwrite like this!"""

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsAuthenticated()]
    #     else:
    #         return [IsAdminUser()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        user = User.objects.get(pk=pk)
        data = AuditLog.objects.all().filter(user=user)
        serializer = AuditLogSerializer(data, many=True)

        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'post', 'delete', 'head', 'options']
    filter_backends = [CustomerFilterBackend]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        # print(self.kwargs)
        return ProductImage.objects.filter(prodcut_id=self.kwargs['product_pk'])


class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_serializer_context(self):
        customer = Customer.objects.get(user_id=self.request.user.id)
        return {'customer_id': customer.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Address.objects.all()
        else:
            return Address.objects.filter(customer__user_id=user.id)


class TransactionViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAdminUser]
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionSerializer
        elif self.request.method == 'PATCH':
            return UpdateTransactionSerializer


class ReportingAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReportingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reporting_data = Reporting(serializer.validated_data)

        total_sales = reporting_data.total_sales()
        favorite_products = list(reporting_data.favorite_products())
        best_cutomer = reporting_data.best_cutomer()
        favorite_collection = list(reporting_data.favorite_collection())
        order_status_counts = list(reporting_data.order_status_counts())

        response_data = {
            'total_sales': total_sales,
            'favorite_products': favorite_products,
            'best_cutomer': best_cutomer,
            'favorite_collection': favorite_collection,
            'order_status_counts': order_status_counts,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SiteSettingsViewSet(ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer


class HomeBannerViewSet(ReadOnlyModelViewSet):
    queryset = HomeBanner.objects.all()
    serializer_class = HomeBannerSerializer


@api_view(['GET'])
def compare_products(request):
    product_ids = request.GET.getlist('product_ids')
    # print(product_ids)
    products = Product.objects.filter(id__in=product_ids)
    data = {}

    productattr = ['Title', 'Price_after_off', 'Collection']
    for attr in productattr:
        product_attrs = {}
        for product in products:
            if attr == 'collection':
                product_attrs[str(product.title)] = str(eval(f'product.{attr.lower()}.title'))
            else:
                product_attrs[str(product.title)] = str(eval(f'product.{attr.lower()}'))

        if attr == 'Price_after_off':
            attr = _('Price')
        if attr == 'Collection':
            attr = _('Collection')
        if attr == 'Title':
            attr = _('Title')

        attr = str(attr)
        data[attr] = product_attrs

    feature_keys = []
    for product in products:
        main_features = MainFeature.objects.filter(product=product)
        for main_feature in main_features:
            # print(main_feature)
            feature_keys.append(main_feature.key)

    for key in feature_keys:
        feature_data = {}
        for product in products:
            # print(product)
            main_features = MainFeature.objects.filter(product=product, key=key)
            if main_features:
                values = []
                for main_feature in main_features:
                    values.append(str(main_feature.value.value))
                feature_data[
                    str(product.title)] = str(', '.join(values))
            else:
                feature_data[str(product.title)] = None
        data[str(key.key)] = feature_data
    # print('data', data)
    return Response(data)


class FeatureViewSet(ModelViewSet):
    queryset = FeatureKey.objects.all()
    serializer_class = FeatureKeyFullSerializer
