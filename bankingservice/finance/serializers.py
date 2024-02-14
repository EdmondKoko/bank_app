from rest_framework import serializers

from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    # StringRelatedField() используется для представления связанных объектов sender и receiver в виде строк.
    # По умолчанию, StringRelatedField() возвращает значение метода __str__() модели
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = '__all__'
