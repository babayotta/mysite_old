import datetime
from django.db import models
from django.conf import settings
from users.models import CustomUser


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
    value = models.FloatField(default=0)
    transaction_type = models.CharField(
        max_length=1,
        choices=TRANSACTION_TYPES,
        default=BUY
    )

    def __str__(self):
        return '{} - {} - {} - {} - {} - {}'.format(
            self.id,
            self.date,
            self.get_transaction_type_display(),
            self.value,
            self.description,
            self.user,
        )
