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
    buy_transactions = transactions.filter(transaction_type=Transaction.BUY)
    for date in [datetime.date(today.year, today.month, day) for day in range(1, number_of_days+1)]:
        buy_transactions_for_date = buy_transactions.filter(date=date)
        buys.append(Entry(
            date,
            buy_transactions_for_date,
            buy_transactions_for_date.aggregate(Sum('cash'))['cash__sum']
        ))

    taxes = []
    tax_transactions = transactions.filter(transaction_type=Transaction.TAX)
    for date in [query.date for query in tax_transactions.order_by('date').distinct('date')]:
        taxes.append(Entry(
            date,
            tax_transactions.filter(date=date),
            tax_transactions.filter(date=date).aggregate(Sum('cash'))['cash__sum']
        ))

    profits = []
    profit_transactions = transactions.filter(transaction_type=Transaction.PROFIT)
    for date in [query.date for query in profit_transactions.order_by('date').distinct('date')]:
        profits.append(Entry(
            date,
            profit_transactions.filter(date=date),
            profit_transactions.filter(date=date).aggregate(Sum('cash'))['cash__sum']
        ))

    buys_sum = buy_transactions.aggregate(Sum('cash'))['cash__sum']
    taxes_sum = tax_transactions.aggregate(Sum('cash'))['cash__sum']
    profits_sum = profit_transactions.aggregate(Sum('cash'))['cash__sum']

    context = {
        'buys': buys,
        'taxes': taxes,
        'profits': profits,
        'buys_sum': buys_sum,
        'taxes_sum': taxes_sum,
        'profits_sum': profits_sum,
    }
    return render(request, 'tyb/current_month.html', context)
