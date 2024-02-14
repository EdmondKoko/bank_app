# bank_app

Создание счета:

POST http://127.0.0.1:8000/api/accounts/

{"name": "Новый счет", "balance": 1000}


Просмотр всех счетов:

GET http://your-domain.com/api/accounts/


Проведение транзакции:

POST http://your-domain.com/api/transactions/

{"sender": 1,
"receiver": 2, "amount": 100}


Просмотр всех транзакций:

GET http://your-domain.com/api/transactions/


Просмотр транзакций для конкретного счета:

GET http://your-domain.com/api/accounts/1/sent_transactions/
GET http://your-domain.com/api/accounts/1/received_transactions/