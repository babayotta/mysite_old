from django import forms
from tyb.models import Transaction
from users.models import CustomUser


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'transaction_type', 'description', 'value']
        user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput())
        widgets = {
            'date': forms.SelectDateWidget(),
        }
