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


class EntryBuy:
    def __init__(self, date, transactions, transactions_sum, budget_for_day):
        self.date = date
        self.transactions = transactions
        self.transactions_sum = transactions_sum
        self.budget_for_day = round(budget_for_day, 2)
        self.balance = round(budget_for_day - transactions_sum, 2)


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')
    today = datetime.date.today()
    user = request.user
    _, number_of_days = monthrange(today.year, today.month)

    transactions = Transaction.objects.filter(user=user, date__year=today.year, date__month=today.month)

    buy_transactions = transactions.filter(transaction_type=Transaction.BUY)
    tax_transactions = transactions.filter(transaction_type=Transaction.TAX)
    profit_transactions = transactions.filter(transaction_type=Transaction.PROFIT)

    buys_sum = buy_transactions.aggregate(Sum('cash'))['cash__sum']
    taxes_sum = tax_transactions.aggregate(Sum('cash'))['cash__sum']
    profits_sum = profit_transactions.aggregate(Sum('cash'))['cash__sum']

    previous_transactions = Transaction.objects.filter(user=user, date__lt=today.replace(day=1))

    previous_buys = previous_transactions.filter(transaction_type=Transaction.BUY).aggregate(Sum('cash'))['cash__sum']
    previous_buys = previous_buys if isinstance(previous_buys, float) else 0
    previous_taxes = previous_transactions.filter(transaction_type=Transaction.TAX).aggregate(Sum('cash'))['cash__sum']
    previous_taxes = previous_taxes if isinstance(previous_taxes, float) else 0
    previous_profits = previous_transactions.filter(transaction_type=Transaction.PROFIT).aggregate(Sum('cash'))['cash__sum']
    previous_profits = previous_profits if isinstance(previous_profits, float) else 0

    previous_sum = round(previous_profits - previous_taxes - previous_buys, 2)
    profits_sum = round(previous_sum + profits_sum, 2)

    budget_for_day = (profits_sum - taxes_sum) / number_of_days

    buys = []
    for date in [datetime.date(today.year, today.month, day) for day in range(1, number_of_days+1)]:
        buy_transactions_for_date = buy_transactions.filter(date=date)
        transactions_sum = buy_transactions_for_date.aggregate(Sum('cash'))['cash__sum']
        buys.append(EntryBuy(
            date,
            buy_transactions_for_date,
            transactions_sum if isinstance(transactions_sum, float) else 0,
            budget_for_day,
        ))

    taxes = []
    for date in [query.date for query in tax_transactions.order_by('date').distinct('date')]:
        tax_transactions_for_date = tax_transactions.filter(date=date)
        taxes.append(Entry(
            date,
            tax_transactions_for_date,
            tax_transactions_for_date.aggregate(Sum('cash'))['cash__sum'],
        ))

    profits = []
    for date in [query.date for query in profit_transactions.order_by('date').distinct('date')]:
        profit_transactions_for_date = profit_transactions.filter(date=date)
        profits.append(Entry(
            date,
            profit_transactions_for_date,
            profit_transactions_for_date.aggregate(Sum('cash'))['cash__sum'],
        ))


    profits.append(Entry(
        today.replace(day=1),
        [Transaction(description='Previous months.', cash=previous_sum)],
        previous_sum,
    ))

    context = {
        'buys': buys,
        'taxes': taxes,
        'profits': profits,
        'buys_sum': buys_sum,
        'taxes_sum': taxes_sum,
        'profits_sum': profits_sum,
    }
    return render(request, 'tyb/current_month.html', context)
