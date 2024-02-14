from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from shop.serializers import CustomerSerializer

from .models import Blog, BlogComment


class BlogSerializer(TranslatableModelSerializer):
    views = serializers.IntegerField(read_only=True)
    author = CustomerSerializer()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'thumbnail', 'views', 'author', 'updated_at')


class BlogCommentSerializer(TranslatableModelSerializer):
    blog = BlogSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ['id', 'customer', 'blog', 'subject', 'message', 'active', 'created_at']
