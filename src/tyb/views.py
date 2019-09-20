import datetime
from calendar import monthrange
from django.shortcuts import render
from django.db.models import Sum, Q, Value as V
from django.db.models.functions import Coalesce
from tyb.models import Transaction


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
    tax_transactions = transactions.filter(transaction_type=Transaction.TAX).order_by('date')
    profit_transactions = transactions.filter(transaction_type=Transaction.PROFIT).order_by('date')

    transactions_sums = transactions.aggregate(
        profit_sum=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)),
        tax_sum=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)),
        buy_sum=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )

    previous_sum = Transaction.objects.filter(user=user, date__lt=today.replace(day=1)).aggregate(
        cash=
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )['cash']

    transactions_sums['profit_sum'] += round(previous_sum, 2)

    budget_for_month = [0 for day in range(number_of_days)]
    remaining_days = number_of_days
    balance_for_day = previous_sum
    buys = []
    for day in range(number_of_days):
        date = today.replace(day=day+1)
        buy_transactions_for_date = buy_transactions.filter(date=date)

        profit_for_day = profit_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']
        tax_for_day = tax_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']
        buy_for_day = buy_transactions.filter(date=date).aggregate(
            cash=Coalesce(Sum('cash'), V(0)))['cash']

        budget_for_day = (profit_for_day - tax_for_day + balance_for_day) / remaining_days
        for i in range(day, number_of_days):
            budget_for_month[i] += round(budget_for_day, 0)
        balance_for_day = budget_for_month[day] - buy_for_day
        remaining_days -= 1

        buys.append(EntryBuy(
            date=date,
            transactions=buy_transactions_for_date,
            transactions_sum=buy_for_day,
            budget_for_day=budget_for_month[day],
            balance_for_day=balance_for_day
        ))

    context = {
        'buys': buys,
        'taxes': tax_transactions,
        'profits': profit_transactions,
        'buys_sum': transactions_sums['buy_sum'],
        'taxes_sum': transactions_sums['tax_sum'],
        'profits_sum': transactions_sums['profit_sum'],
        'previous_sum': round(previous_sum, 2),
    }
    return render(request, 'tyb/current_month.html', context)
