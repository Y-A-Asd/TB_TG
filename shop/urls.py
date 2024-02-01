from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import AddressViewSet, TransactionViewSet, PromotionViewSet, ReportingAPIView

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'transactions', TransactionViewSet)
router.register(r'promotions', PromotionViewSet)

cart_router = routers.NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product_reviews')
product_router.register('images', views.ProductImageViewSet, basename='product_images')

urlpatterns = [
    *router.urls,
    *product_router.urls,
    *cart_router.urls,
    path('reporting/', ReportingAPIView.as_view(), name='reporting'),
]
