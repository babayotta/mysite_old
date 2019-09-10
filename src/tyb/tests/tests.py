import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from tyb.models import Transaction
from tyb.tests.factories import TransactionFactory
from users.tests.factories import CustomUserFactory


class TransactionModelTest(TestCase):
    def test_transaction_has_a_valid_creation_date(self):
        user = get_user_model()
        transaction = Transaction(user)
        self.assertEqual(transaction.date, datetime.date.today())


class TransactionManagerTests(TestCase):
    def test_get_all_user_transactions(self):
        user = CustomUserFactory()
        TransactionFactory.create_batch(3, user=user)
        TransactionFactory.create_batch(5)

        valid_queryset = []
        for query in Transaction.objects.filter(user=user):
            valid_queryset.append('<Transaction: %s>' % query)
        self.assertQuerysetEqual(
            Transaction.user_transactions.get_queryset(user),
            valid_queryset,
            ordered=False
        )
