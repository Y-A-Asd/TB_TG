from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

cart_router = routers.NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product_reviews')

urlpatterns = router.urls + product_router.urls + cart_router.urls
