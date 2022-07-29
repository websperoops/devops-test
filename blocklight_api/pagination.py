from rest_framework import pagination

class TimelineResultsCustomPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'count'
    max_page_size = 50