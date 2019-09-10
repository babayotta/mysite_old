from django.shortcuts import render
from django.http import HttpResponse
from tyb.models import Transaction


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    transactions = Transaction.user_transactions.current_month(request.user)
    context = {'transactions': transactions}
    return render(request, 'tyb/current_month.html', context)
