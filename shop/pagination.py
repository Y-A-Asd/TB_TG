from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
        remember to fix pagination in blog and product list views js
    """
    page_size = 2
