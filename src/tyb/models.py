from django.db import models
from django.conf import settings


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.CharField(max_length=300)
    cash = models.FloatField()
    trans_type = models.BooleanField()
