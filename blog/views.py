from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from blog.models import BlogComment, Blog
from blog.serializers import BlogSerializer, BlogCommentSerializer
from shop.pagination import DefaultPagination


# Create your views here.
class BlogViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Blog.objects.all().prefetch_related('author', 'comments')
    serializer_class = BlogSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['translations__title', 'translations__body']
    ordering = ['-updated_at']


class BlogCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'message']
    ordering = ['-updated_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'blog_id': self.kwargs['blog_pk'], 'user_id': self.request.user.id}

    def get_queryset(self):
        print(self.kwargs)
        return BlogComment.objects.all().select_related('customer', 'blog').filter(blog_id=self.kwargs['blog_pk'],
                                                                                   active=True)
