from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """Менеджмент счетов через API."""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # Добавляет новые действия к AccountViewSet, которые возвращают все отправленные
    # и полученные транзакции для конкретного счета
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

    # Добавляет новое действие к AccountViewSet, которое переключает статус блокировки счета
    @action(detail=True, methods=['post'])
    def account_block(self, request, pk=None):
        account = self.get_object()
        account.is_blocked = not account.is_blocked
        account.save()
        return Response({'status': 'Счет заблокирован' if account.is_blocked else 'Счет разблокирован'})


class TransactionViewSet(viewsets.ModelViewSet):
    """Менеджмент транзакций между счетами через API."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # При проведении транзакции, проверяется существование отправителя и получателя,
    # а также достаточность баланса у отправителя. Если все проверки проходят успешно,
    # балансы счетов обновляются, и транзакция сохраняется в базе данных
    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        amount = Decimal(request.data.get('amount'))

        if amount < 0:
            raise ValidationError("Сумма транзакции не может быть меньше или равной нулю.")

        try:
            sender = Account.objects.get(id=sender_id)
            receiver = Account.objects.get(id=receiver_id)
        except Account.DoesNotExist:
            raise NotFound("Отправитель или получатель не существует.")

        if sender.is_blocked or receiver.is_blocked:
            raise PermissionDenied("Один из счетов заблокирован.")

        if sender.balance < amount:
            raise ValidationError("Недостаточный баланс у отправителя.")

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        return super().create(request, *args, **kwargs)
