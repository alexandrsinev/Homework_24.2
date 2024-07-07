from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 100
    max_page_size = 100
