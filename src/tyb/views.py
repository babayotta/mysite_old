import datetime
from django.shortcuts import render
from django.http import HttpResponse
from tyb.models import Transaction


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')
    today = datetime.date.today()
    transactions = Transaction.user_transactions.get_month(request.user, today.month)
    context = {'transactions': transactions}
    return render(request, 'tyb/current_month.html', context)
