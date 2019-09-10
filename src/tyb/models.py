import datetime
from django.db import models
from django.conf import settings
from users.models import CustomUser


class TransactionManager(models.Manager):
    def get_queryset(self, user: CustomUser):
        return super(TransactionManager, self).get_queryset().filter(user=user)

    def current_month(self, user: CustomUser):
        today = datetime.date.today()
        return self.get_queryset(user).filter(date__month=today.month)


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
        return '{} - {} - {}'.format(
            self.get_transaction_type_display(),
            self.cash,
            self.description,
        )
