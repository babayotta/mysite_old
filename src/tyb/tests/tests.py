import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from tyb.models import Transaction


class TransactionModelTest(TestCase):

    def test_transaction_has_a_valid_creation_date(self):
        user = get_user_model()
        transaction = Transaction(user)
        self.assertEqual(transaction.date, datetime.date.today())
