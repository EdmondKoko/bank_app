![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-2.2.6-red?style=for-the-badge&logo=django&logoColor=blue)
![SQLite](https://img.shields.io/badge/SQLite-grey?style=for-the-badge&logo=postgresql&logoColor=yellow)
![Pytest-django](https://img.shields.io/badge/pytest-django==3.8.0-orange?style=for-the-badge&logo=nginx&logoColor=green)

# Приложение банковского сервиса

## Описание:
Приложение позволяет создавать счета и проводить транзакции между ними и отслеживать состояние счета.
Так же отслеживать все транзакции, транзакции для конкретного счета, входящие и исходящие транзакции

Реализация API:
Создание нового банковского счета.
Просмотр всех счетов в системе.
Просмотр всех транзакций в системе.
Проведение транзакции между счетами.
Просмотр всех транзакций для конкретного счета.

Обеспечение корректной работы операций:
Проверка существования отправителя и получателя.
При создании счета, баланс равен 0.
Обновление балансов счетов при проведении транзакции.
Обработка случаев недостаточного баланса у отправителя.
Ведение истории транзакций для каждого счета.


### Запуск приложения:

Клонируем проект:

```bash
git clone https://github.com/EdmondKoko/bank_app
```

Переходим в папку с проектом:

```bash
cd bankingservice
```

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/bin/activate
```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Запускаем проект:

```bash
python manage.py runserver
```

После чего проект будет доступен по адресу (http://127.0.0.1:8000/)

### Примеры запросов API
Создание счета:
```bash
POST http://127.0.0.1:8000/api/accounts/

{    "name": "Новый счет",
     "balance": 1000
     }
```
Просмотр всех счетов:
```bash
GET http://your-domain.com/api/accounts/
```

Проведение транзакции:
```bash
POST http://your-domain.com/api/transactions/

{    "sender": 1,
     "receiver": 2,
     "amount": 100
     }
```

Просмотр всех транзакций:
```bash
GET http://your-domain.com/api/transactions/
```

Просмотр транзакций для конкретного счета:
```bash
GET http://your-domain.com/api/accounts/1/sent_transactions/
```
```bash
GET http://your-domain.com/api/accounts/1/received_transactions/
```

Для блокировки или разблокировки счета:
```bash
POST http://your-domain.com/api/accounts/1/account_block/
```