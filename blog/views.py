from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.viewsets import GenericViewSet
from blog.models import BlogComment, Blog
from blog.serializers import BlogSerializer, BlogCommentSerializer
from shop.pagination import DefaultPagination


# Create your views here.
class BlogViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['title', 'body', 'author']
    ordering = ['-updated_at']


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'message']
    ordering_fields = ['subject', 'message', 'customer']
    ordering = ['-updated_at']
