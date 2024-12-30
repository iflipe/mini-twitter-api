from rest_framework.pagination import CursorPagination


# Organiza a página de listagem de posts (timeline) por ordem de criação e limita a 50 posts por página
class TimelinePagination(CursorPagination):
    page_size = 50
    ordering = "-created_at"
