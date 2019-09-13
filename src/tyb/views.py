import datetime
from django.shortcuts import render
from tyb.models import Transaction


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')
    today = datetime.date.today()
    user = request.user
    transactions = Transaction.user_transactions.get_transactions_for_month(user, today)
    buys_sum = Transaction.user_transactions.get_sum_of_transactions_by_type_for_month(
        user, today, Transaction.BUY
    )
    taxes_sum = Transaction.user_transactions.get_sum_of_transactions_by_type_for_month(
        user, today, Transaction.TAX
    )
    profits_sum = Transaction.user_transactions.get_sum_of_transactions_by_type_for_month(
        user, today, Transaction.PROFIT
    )
    context = {
        'transactions': transactions,
        'buys_sum': buys_sum['cash__sum'],
        'taxes_sum': taxes_sum['cash__sum'],
        'profits_sum': profits_sum['cash__sum'],
    }
    return render(request, 'tyb/current_month.html', context)
