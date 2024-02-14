from django.urls import path, include
from . import views

app_name = 'front'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp'),
    path('set-password/', views.SetPasswordView.as_view(), name='set-password'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='products-detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order-detail/<int:id>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('compare/', views.CompareView.as_view(), name='compare'),
    path('', views.HomeView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('set_language/', views.set_language, name='set_language'),
    path('blogs/<int:id>/', views.BlogDetailView.as_view(), name='blog_detail'),

]
# todo: 1. implement remaining:{profile - make order from cart}
# todo: 2. link routes inside site
# todo: 2.1. caching
# todo: 3. valid error message
# todo: 4. translations
# todo: 5. gold
# todo: 6(optional). blog
# todo: 7(optional). wishlist
