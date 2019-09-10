import random
import factory
from tyb.models import Transaction
from users.tests.factories import CustomUserFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.LazyAttribute(lambda o: CustomUserFactory())
    date = factory.Faker('date_between', start_date='-30d', end_date='today')
    description = factory.Faker('sentence', nb_words=5)
    cash = factory.LazyAttribute(lambda o: random.randrange(1000))
    transaction_type = factory.LazyAttribute(
        lambda o: random.choice([Transaction.PROFIT, Transaction.TAX, Transaction.BUY])
    )
