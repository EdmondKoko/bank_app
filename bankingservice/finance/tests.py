from django.test import TestCase
from rest_framework.test import APIClient

from .models import Account, Transaction


class TransactionTestCase(TestCase):
    """TransactionTestCase - это класс тестового случая, который наследуется от TestCase.
    Метод setUp выполняется перед каждым тестовым методом и используется для
    настройки начального состояния для тестов."""

    def setUp(self):
        self.client = APIClient()
        self.account1 = Account.objects.create(name='Account 1',
                                               balance=1000)
        self.account2 = Account.objects.create(name='Account 2',
                                               balance=1000)

    def test_create_transaction(self):
        """Тест проверяет успешное создание транзакции. В нем выполняется POST-запрос к API с данными
        для новой транзакции. Затем проверяется, что ответ API имеет статус 201
        (что означает успешное создание), что количество транзакций в базе данных увеличилось на одну,
        и что балансы счетов отправителя и получателя были корректно обновлены."""

        response = self.client.post('/api/transactions/', {
            'sender': self.account1.id,
            'receiver': self.account2.id,
            'amount': 200,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 800)
        self.assertEqual(self.account2.balance, 1200)

    def test_insufficient_balance(self):
        """Тест проверяет сценарий, когда у отправителя недостаточно средств для выполнения
        транзакции. В нем выполняется POST-запрос к API с данными для новой транзакции, где сумма
        транзакции превышает баланс отправителя. Затем проверяется, что ответ API имеет статус 400
        (что означает ошибку клиента), что количество транзакций в базе данных не изменилось, и что
        балансы счетов отправителя и получателя остались без изменений."""

        response = self.client.post('/api/transactions/', {
            'sender': self.account1.id,
            'receiver': self.account2.id,
            'amount': 2000,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 1000)

    def test_account_blocking(self):
        """Тест проверяет, что транзакции не могут быть выполнены, если счет отправителя заблокирован"""
        self.account1.is_blocked = True
        self.account1.save()
        response = self.client.post('/api/transactions/', {
            'sender': self.account1.id,
            'receiver': self.account2.id,
            'amount': 200,
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 1000)

    def test_negative_amount(self):
        """Тест проверяет, что транзакции не могут быть выполнены, если сумма транзакции отрицательная"""
        response = self.client.post('/api/transactions/', {
            'sender': self.account1.id,
            'receiver': self.account2.id,
            'amount': -200,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

