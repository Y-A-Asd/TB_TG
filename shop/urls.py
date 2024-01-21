from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>', views.products_detail),
    path('collections/', views.collection_list),
    path('collections/<int:pk>', views.collection_detail),

]