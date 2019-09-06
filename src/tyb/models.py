from django.db import models
from django.conf import settings


class Transaction(models.Model):
    PROFIT = 'P'
    TAX = 'T'
    BUY = 'B'
    TRANSACTION_TYPES = (
        (PROFIT, 'Profit'),
        (TAX, 'Tax'),
        (BUY, 'Buy'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.CharField(max_length=300)
    cash = models.FloatField()
    transaction_type = models.CharField(max_length=1,
                                        choices=TRANSACTION_TYPES,
                                        default=BUY)
