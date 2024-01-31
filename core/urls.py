from django.urls import path, include
from .views import UserCreateView, VerifyOtpView

urlpatterns = [
    path('users/', UserCreateView.as_view({'post': 'create'}), name='user_create'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.jwt')),
]