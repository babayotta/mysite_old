import datetime
from calendar import monthrange
from django.shortcuts import render
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from tyb.models import Transaction


class Entry:
    def __init__(self, date, transactions, transactions_sum):
        self.date = date
        self.transactions = transactions
        self.transactions_sum = transactions_sum


class EntryBuy:
    def __init__(self, date, transactions, transactions_sum, budget_for_day, balance_for_day):
        self.date = date
        self.transactions = transactions
        self.transactions_sum = transactions_sum
        self.budget_for_day = budget_for_day
        self.balance_for_day = balance_for_day


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

    buys_sum = buy_transactions.aggregate(cash=Coalesce(Sum('cash'), V(0)))['cash']
    taxes_sum = tax_transactions.aggregate(cash=Coalesce(Sum('cash'), V(0)))['cash']
    profits_sum = profit_transactions.aggregate(cash=Coalesce(Sum('cash'), V(0)))['cash']

    previous_transactions = Transaction.objects.filter(user=user, date__lt=today.replace(day=1))

    previous_buys = previous_transactions.filter(transaction_type=Transaction.BUY).aggregate(
        cash=Coalesce(Sum('cash'), V(0)))['cash']
    previous_taxes = previous_transactions.filter(transaction_type=Transaction.TAX).aggregate(
        cash=Coalesce(Sum('cash'), V(0)))['cash']
    previous_profits = previous_transactions.filter(transaction_type=Transaction.PROFIT).aggregate(
        cash=Coalesce(Sum('cash'), V(0)))['cash']

    previous_sum = previous_profits - previous_taxes - previous_buys
    profits_sum = round(previous_sum + profits_sum, 2)

    budget_for_month = [0 for day in range(number_of_days)]
    balance_for_month = [0 for day in range(number_of_days)]
    remaining_days = number_of_days
    balance_for_day = previous_sum
    for day in range(1, number_of_days + 1):
        date = today.replace(day=day)

        profit_for_day = profit_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']
        tax_for_day = tax_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']
        buy_for_day = buy_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']

        budget_for_day = (profit_for_day - tax_for_day + balance_for_day) / remaining_days
        for i in range(day-1, number_of_days):
            budget_for_month[i] += round(budget_for_day, 0)
        balance_for_day = budget_for_month[day-1] - buy_for_day
        balance_for_month[day-1] += round(balance_for_day, 2)
        remaining_days -= 1

    buys = []
    for date in [datetime.date(today.year, today.month, day) for day in range(1, number_of_days+1)]:
        buy_transactions_for_date = buy_transactions.filter(date=date)
        transactions_sum = buy_transactions_for_date.aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']
        buys.append(EntryBuy(
            date=date,
            transactions=buy_transactions_for_date,
            transactions_sum=transactions_sum,
            budget_for_day=budget_for_month[date.day-1],
            balance_for_day=balance_for_month[date.day-1]
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
        [Transaction(description='Previous months.', cash=round(previous_sum, 2))],
        round(previous_sum, 2),
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
