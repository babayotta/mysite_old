import datetime
from django.db import models
from django.conf import settings
from users.models import CustomUser


class TransactionManager(models.Manager):
    def get_queryset(self, user: CustomUser):
        return super(TransactionManager, self).get_queryset().filter(user=user)

    def get_transactions_for_month(self, user: CustomUser, month: int):
        return self.get_queryset(user).filter(date__month=month)

    def get_transactions_by_type_for_month(
            self,
            user: CustomUser,
            month: int,
            transaction_type: str
    ):
        return self.get_transactions_for_month(user, month).filter(transaction_type=transaction_type)

    def get_sum_of_transactions_by_type_for_month(
            self,
            user: CustomUser,
            month: int,
            transaction_type: str
    ):
        return self.get_transactions_by_type_for_month(user, month, transaction_type
                                                       ).aggregate(models.Sum('cash'))


class Transaction(models.Model):
    PROFIT = 'P'
    TAX = 'T'
    BUY = 'B'
    TRANSACTION_TYPES = (
        (PROFIT, 'Profit'),
        (TAX, 'Tax'),
        (BUY, 'Buy'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    description = models.CharField(max_length=300, default='Some description.')
    cash = models.FloatField(default=0)
    transaction_type = models.CharField(
        max_length=1,
        choices=TRANSACTION_TYPES,
        default=BUY
    )
    objects = models.Manager()
    user_transactions = TransactionManager()

    def __str__(self):
        return '{} - {} - {} - {}'.format(
            self.date,
            self.get_transaction_type_display(),
            self.cash,
            self.description,
        )
