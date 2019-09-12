import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from tyb.tests.factories import *
from tyb.models import Transaction
from users.tests.factories import CustomUserFactory


class TransactionModelTest(TestCase):
    def test_transaction_has_a_valid_creation_date(self):
        user = get_user_model()
        transaction = Transaction(user)
        self.assertEqual(transaction.date, datetime.date.today())


class TransactionManagerTests(TestCase):
    def test_get_queryset(self):
        user = CustomUserFactory()
        TransactionFactoryCurrentYear.create_batch(5)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentYear.create_batch(3, user=user):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_queryset(user),
            valid_queryset,
            ordered=False
        )

    def test_get_transactions_for_current_month(self):
        user = CustomUserFactory()
        today = datetime.date.today()
        delta = datetime.timedelta(days=50)
        TransactionFactoryCurrentMonth.create_batch(5, user=user, date=today-delta)
        TransactionFactoryCurrentYear.create_batch(5)
        TransactionFactoryCurrentMonth.create_batch(5)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentMonth.create_batch(3, user=user):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_transactions_for_month(user, today.month),
            valid_queryset,
            ordered=False
        )

    def test_get_transactions_by_type_for_month(self):
        pass

    def test_get_sum_of_transactions_by_type_for_month(self):
        pass
