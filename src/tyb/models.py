from django.db import models
from django.contrib.auth import get_user_model


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.CharField(max_length=300)
    cash = models.FloatField()
    trans_type = models.BooleanField()
