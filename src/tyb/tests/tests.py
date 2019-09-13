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

    def test_get_transactions_for_year(self):
        user = CustomUserFactory()
        today = datetime.date.today()
        TransactionFactoryWithoutCurrentYear.create_batch(5)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentYear.create_batch(3, user=user):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_transactions_for_year(user, today),
            valid_queryset,
            ordered=False
        )

    def test_get_transactions_for_month(self):
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
            Transaction.user_transactions.get_transactions_for_month(user, today),
            valid_queryset,
            ordered=False
        )

    def test_get_transactions_by_type_for_month(self):
        user = CustomUserFactory()
        today = datetime.date.today()
        TransactionFactoryCurrentMonth.create_batch(5, user=user, transaction_type=Transaction.TAX)
        TransactionFactoryCurrentMonth.create_batch(5, user=user, transaction_type=Transaction.PROFIT)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentMonth.create_batch(3, user=user,
                                                                       transaction_type=Transaction.BUY):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_transactions_by_type_for_month(user, today, Transaction.BUY),
            valid_queryset,
            ordered=False
        )

    def test_get_sum_of_transactions_by_type_for_month(self):
        user = CustomUserFactory()
        today = datetime.date.today()
        TransactionFactoryCurrentMonth.create_batch(5, user=user, transaction_type=Transaction.TAX, cash=123)
        TransactionFactoryCurrentMonth.create_batch(3, user=user, transaction_type=Transaction.BUY, cash=123)

        valid_sum = {'cash__sum': 369}

        self.assertEqual(
            Transaction.user_transactions.get_sum_of_transactions_by_type_for_month(user, today,
                                                                                    Transaction.BUY),
            valid_sum
        )
