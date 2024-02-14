from rest_framework.response import Response
from rest_framework import viewsets, status
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
    # при создании счета, баланс автоматически устанавливается равным 0 благодаря параметру default=0 в модели Account.
    # При проведении транзакции, проверяется существование отправителя и получателя, а также достаточность баланса у
    # отправителя. Если все проверки проходят успешно,
    # балансы счетов обновляются, и транзакция сохраняется в базе данных
    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        amount = request.data.get('amount')

        try:
            sender = Account.objects.get(id=sender_id)
            receiver = Account.objects.get(id=receiver_id)
        except Account.DoesNotExist:
            return Response({"error": "Отправитель или получатель не существует."},
                            status=status.HTTP_400_BAD_REQUEST)

        if sender.is_blocked or receiver.is_blocked:
            return Response({"error": "Один из счетов заблокирован."},
                            status=status.HTTP_400_BAD_REQUEST)

        if sender.balance < amount:
            return Response({"error": "Недостаточный баланс у отправителя."},
                            status=status.HTTP_400_BAD_REQUEST)

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        return super().create(request, *args, **kwargs)
