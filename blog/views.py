from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from blog.models import BlogComment, Blog
from blog.serializers import BlogSerializer, BlogCommentSerializer
from shop.pagination import DefaultBlogPagination


# Create your views here.
class BlogViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Blog.objects.all().prefetch_related('author', 'comments')
    serializer_class = BlogSerializer
    pagination_class = DefaultBlogPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['translations__title', 'translations__body']
    ordering = ['-updated_at']

    # https://stackoverflow.com/questions/56228485/how-can-i-make-a-view-count-in-django-rest-framework
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
