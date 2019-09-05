from django.db import models


class Transaction(models.Model):
    date = models.DateTimeField()
    description = models.CharField(max_length=300)
    amount = models.FloatField()
    trans_type = models.BooleanField()
