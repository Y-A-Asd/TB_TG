from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from shop.models import Customer
from shop.serializers import CustomerSerializer

from .models import Blog, BlogComment


class BlogSerializer(TranslatableModelSerializer):
    views = serializers.IntegerField(read_only=True)
    author = CustomerSerializer()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'thumbnail', 'views', 'author', 'updated_at')


class BlogCommentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ['id', 'customer', 'subject', 'message', 'created_at']

    def create(self, validated_data):
        blog_id = self.context['blog_id']
        try:
            customer = Customer.objects.get(user_id=self.context['user_id'])
        except Customer.DoesNotExist:
            raise serializers.ValidationError(_('User not found'))
        return BlogComment.objects.create(blog_id=blog_id, customer=customer, **validated_data)
