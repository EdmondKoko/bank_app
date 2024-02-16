from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  default=0)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    sender = models.ForeignKey(Account,
                               on_delete=models.CASCADE,
                               related_name='sent_transactions')
    receiver = models.ForeignKey(Account,
                                 on_delete=models.CASCADE,
                                 related_name='received_transactions')
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} for {self.amount}'
