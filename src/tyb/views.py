import datetime
from calendar import  monthrange
from django.shortcuts import render
from django.db.models import Sum
from tyb.models import Transaction


class Entry:
    def __init__(self, date, transactions, transactions_sum):
        self.date = date
        self.transactions = transactions
        self.transactions_sum = transactions_sum


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')
    today = datetime.date.today()
    user = request.user
    _, number_of_days = monthrange(today.year, today.month)

    transactions = Transaction.objects.filter(user=user, date__year=today.year, date__month=today.month)

    buys = []
    for date in [datetime.date(today.year, today.month, day) for day in range(1, number_of_days+1)]:
        print(transactions.filter(transaction_type=Transaction.BUY, date=date).aggregate(Sum('cash'))['cash__sum'])
        buys.append(Entry(
            date,
            transactions.filter(transaction_type=Transaction.BUY, date=date),
            transactions.filter(transaction_type=Transaction.BUY, date=date).aggregate(Sum('cash'))['cash__sum']
        ))

    buys_sum = transactions.filter(transaction_type=Transaction.BUY).aggregate(Sum('cash'))
    taxes_sum = transactions.filter(transaction_type=Transaction.TAX).aggregate(Sum('cash'))
    profits_sum = transactions.filter(transaction_type=Transaction.PROFIT).aggregate(Sum('cash'))

    context = {
        'buys': buys,
        'buys_sum': buys_sum['cash__sum'],
        'taxes_sum': taxes_sum['cash__sum'],
        'profits_sum': profits_sum['cash__sum'],
    }
    return render(request, 'tyb/current_month.html', context)
