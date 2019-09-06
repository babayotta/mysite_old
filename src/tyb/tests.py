import datetime

from django.test import TestCase

from users.models import CustomUser
from tyb.models import Transaction


class TransactionModelTest(TestCase):

    def test_transaction_has_a_valid_creation_date(self):
        user = CustomUser()
        transaction = Transaction(user)
        self.assertEqual(transaction.date, datetime.date.today())
