from rest_framework.pagination import PageNumberPagination


class SmallPagesPagination(PageNumberPagination):
    page_size = 20

class SmallestPagesPagination(PageNumberPagination):
    page_size = 7