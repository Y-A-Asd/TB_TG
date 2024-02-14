from django.urls import path
from rest_framework_nested import routers
from .views import BlogViewSet, BlogCommentViewSet

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blogs')
blog = routers.NestedDefaultRouter(router, 'blogs', lookup='blog')

blog.register(r'comments', BlogCommentViewSet, basename='blog_comments')

app_name = 'blog'
urlpatterns = [
    *router.urls,
    *blog.urls
]
