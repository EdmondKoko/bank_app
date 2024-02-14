from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # @action(detail=True, methods=['get']) добавляет новые действия к AccountViewSet,
    # которые возвращают все отправленные и полученные транзакции для конкретного счета.
    @action(detail=True, methods=['get'])
    def sent_transactions(self, request, pk=None):
        account = self.get_object()
        transactions = Transaction.objects.filter(sender=account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def received_transactions(self, request, pk=None):
        account = self.get_object()
        transactions = Transaction.objects.filter(receiver=account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
