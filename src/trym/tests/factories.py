import random
import factory
from trym.models import Transaction
from users.tests.factories import CustomUserFactory


class TransactionFactoryCurrentMonth(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.LazyAttribute(lambda o: CustomUserFactory())
    date = factory.Faker('date_this_month', before_today=True, after_today=True)
    description = factory.Faker('sentence', nb_words=5)
    value = factory.Faker('pyfloat', right_digits=2, positive=True, min_value=0, max_value=3000)
    transaction_type = factory.LazyAttribute(
        lambda o: random.choice([Transaction.PROFIT, Transaction.TAX, Transaction.BUY])
    )


class TransactionFactoryCurrentYear(TransactionFactoryCurrentMonth):
    date = factory.Faker('date_this_year', before_today=True, after_today=True)


class TransactionFactoryWithoutCurrentYear(TransactionFactoryCurrentMonth):
    date = factory.Faker('date_between', start_date='-3y', end_date='-1y')
