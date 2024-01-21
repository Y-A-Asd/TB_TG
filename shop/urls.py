from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product_pk')
product_router.register('reviews', views.ReviewViewSet, basename='product_reviews')

urlpatterns = router.urls +product_router.urls