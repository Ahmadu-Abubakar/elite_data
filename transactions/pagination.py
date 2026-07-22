from rest_framework.pagination import CursorPagination


class TransactionHistoryPagination(CursorPagination):
    page_size = 10
    ordering = "-created_at"