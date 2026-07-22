from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .serializers import TransactionHistorySerializer
from .services import get_transaction_history
from .pagination import TransactionHistoryPagination



class TransactionHistoryView(ListAPIView):

    serializer_class = TransactionHistorySerializer
    permission_class = [IsAuthenticated]
    pagination_class = TransactionHistoryPagination

    def get_queryset(self):
        return get_transaction_history(self.request.user)

# Create your views here.
