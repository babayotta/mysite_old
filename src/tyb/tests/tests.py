import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from tyb.models import Transaction
from tyb.tests.factories import TransactionFactoryCurrentMonth
from users.tests.factories import CustomUserFactory


class TransactionModelTest(TestCase):
    def test_transaction_has_a_valid_creation_date(self):
        user = get_user_model()
        transaction = Transaction(user)
        self.assertEqual(transaction.date, datetime.date.today())


class TransactionManagerTests(TestCase):
    def test_get_queryset(self):
        user = CustomUserFactory()
        TransactionFactoryCurrentMonth.create_batch(5)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentMonth.create_batch(3, user=user):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_queryset(user),
            valid_queryset,
            ordered=False
        )

    def test_get_month_with_current_month(self):
        user = CustomUserFactory()
        today = datetime.date.today()
        TransactionFactoryCurrentMonth.create_batch(5, user=user,
                                                    date=today - datetime.timedelta(days=40))
        TransactionFactoryCurrentMonth.create_batch(5)

        valid_queryset = []
        for transaction in TransactionFactoryCurrentMonth.create_batch(3, user=user):
            valid_queryset.append('<Transaction: %s>' % transaction)

        self.assertQuerysetEqual(
            Transaction.user_transactions.get_month(user, today.month),
            valid_queryset,
            ordered=False
        )
