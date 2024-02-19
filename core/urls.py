from django.urls import path, include
from .views import UserCreateView, VerifyOtpView, UserLoginOTPView

app_name = 'core'
urlpatterns = [
    path('users/', UserCreateView.as_view({'post': 'create'}), name='user_create'),
    path('login-otp/', UserLoginOTPView.as_view(), name='login-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.jwt')),
]
