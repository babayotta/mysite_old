import factory
import random
from django.conf import settings


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Faker('email')
    username = factory.LazyAttribute(lambda o: o.email)
    first_day_of_month = factory.LazyAttribute(lambda o: random.randint(1, 31))
