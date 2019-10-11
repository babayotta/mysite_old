from django.forms import ModelForm
from tyb.models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'transaction_type', 'description',]
