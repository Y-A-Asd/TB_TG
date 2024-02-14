from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, BlogCommentViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'comments', BlogCommentViewSet)

app_name = 'blog'
urlpatterns = [
    *router.urls,
]