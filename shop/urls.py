from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register(r'addresses', views.AddressViewSet, basename='addresses')
router.register(r'transactions', views.TransactionViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'site-settings', views.SiteSettingsViewSet)
router.register(r'home-banners', views.HomeBannerViewSet)
router.register(r'features', views.FeatureViewSet, basename='features')

cart_router = routers.NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product_reviews')
product_router.register('images', views.ProductImageViewSet, basename='product_images')

urlpatterns = [
    *router.urls,
    *product_router.urls,
    *cart_router.urls,
    path('reporting/', views.ReportingAPIView.as_view(), name='reporting'),
    path('compare/', views.compare_products, name='compare_products'),
    path('payment-verify/', views.VerifyAPIView.as_view(), name='payment-verify'),
]
