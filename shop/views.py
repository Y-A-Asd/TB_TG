from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product


# Create your views here.

@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
