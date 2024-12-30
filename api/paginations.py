from rest_framework.pagination import CursorPagination


class TimelinePagination(CursorPagination):
    page_size = 50
    ordering = "-created_at"
