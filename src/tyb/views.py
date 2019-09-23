import datetime
from calendar import monthrange
from django.http import JsonResponse
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

    buy_transactions = list(transactions.filter(transaction_type=Transaction.BUY).order_by('date'))
    tax_transactions = list(transactions.filter(transaction_type=Transaction.TAX).order_by('date'))
    profit_transactions = list(transactions.filter(transaction_type=Transaction.PROFIT).order_by('date'))

    transactions_sums = transactions.aggregate(
        profits_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)),
        taxes_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)),
        buys_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )

    previous_total_sum = Transaction.objects.filter(user=user, date__lt=today.replace(day=1)).aggregate(
        cash=
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )['cash']

    transactions_sums['profits_total'] += round(previous_total_sum, 2)

    budget_for_month = [0 for day in range(number_of_days)]
    remaining_days = number_of_days
    balance_for_previous_day = previous_total_sum
    buys = []
    for day in range(number_of_days):
        date = today.replace(day=day+1)
        buy_for_day = 0
        buy_transactions_for_date = []
        for transaction in buy_transactions:
            if transaction.date == date:
                buy_transactions_for_date.append(transaction)
                buy_for_day += transaction.cash

        profit_for_day = 0
        for transaction in profit_transactions:
            if transaction.date == date:
                profit_for_day += transaction.cash

        tax_for_day = 0
        for transaction in tax_transactions:
            if transaction.date == date:
                tax_for_day += transaction.cash

        budget_for_day = (profit_for_day - tax_for_day + balance_for_previous_day) / remaining_days
        for i in range(day, number_of_days):
            budget_for_month[i] += round(budget_for_day, 0)
        balance_for_previous_day = budget_for_month[day] - buy_for_day
        remaining_days -= 1

        buys.append(EntryBuy(
            date=date,
            transactions=buy_transactions_for_date,
            transactions_sum=buy_for_day,
            budget_for_day=budget_for_month[day],
            balance_for_day=balance_for_previous_day
        ))

    context = {
        'buys': buys,
        'taxes': tax_transactions,
        'profits': profit_transactions,
        'buys_total': transactions_sums['buys_total'],
        'taxes_total': transactions_sums['taxes_total'],
        'profits_total': transactions_sums['profits_total'],
        'previous_total_sum': round(previous_total_sum, 2),
    }
    return render(request, 'tyb/current_month.html', context)


def tyb_api(request):
    today = datetime.date.today()
    user = request.user
    _, number_of_days = monthrange(today.year, today.month)

    transactions = Transaction.objects.filter(user=user, date__year=today.year, date__month=today.month)

    buy_transactions = list(
        transactions.filter(transaction_type=Transaction.BUY).order_by('date'))
    tax_transactions = list(
        transactions.filter(transaction_type=Transaction.TAX).order_by('date'))
    profit_transactions = list(
        transactions.filter(transaction_type=Transaction.PROFIT).order_by('date'))

    transactions_sums = transactions.aggregate(
        profits_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)),
        taxes_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)),
        buys_total=Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )

    previous_total_sum = Transaction.objects.filter(user=user, date__lt=today.replace(day=1)).aggregate(
        cash=
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.PROFIT)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.TAX)), V(0)) -
        Coalesce(Sum('cash', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )['cash']

    transactions_sums['profits_total'] += previous_total_sum

    budget_for_days = [0 for day in range(number_of_days)]
    remaining_days = number_of_days
    balance_for_previous_day = previous_total_sum
    buys = []
    taxes = []
    profits = []
    for day in range(number_of_days):
        date = today.replace(day=day + 1)
        sum_buy_for_day = 0
        sum_tax_for_day = 0
        sum_profit_for_day = 0
        buy_transactions_for_day = []
        tax_transactions_for_day = []
        profit_transactions_for_day = []

        for transaction in buy_transactions:
            if transaction.date == date:
                sum_buy_for_day += transaction.cash
                buy_transactions_for_day.append(transaction)
        for transaction in tax_transactions:
            if transaction.date == date:
                sum_tax_for_day += transaction.cash
                tax_transactions_for_day.append(transaction)
        for transaction in profit_transactions:
            if transaction.date == date:
                sum_profit_for_day += transaction.cash
                profit_transactions_for_day.append(transaction)

        budget_for_day = (sum_profit_for_day - sum_tax_for_day + balance_for_previous_day) / remaining_days
        for i in range(day, number_of_days):
            budget_for_days[i] += budget_for_day
        balance_for_previous_day = budget_for_days[day] - sum_buy_for_day
        remaining_days -= 1

        buys.append({
            'date': date,
            'transactions': buy_transactions_for_day,
            'budget_for_day': budget_for_days[day],
            'balance_for_day': balance_for_previous_day,
        })
        if tax_transactions_for_day:
            taxes.append({
                'date': date,
                'transactions': tax_transactions_for_day,
            })
        if profit_transactions_for_day:
            profits.append({
                'date': date,
                'transactions': profit_transactions_for_day,
            })

    table = {
        'buys': buys,
        'taxes': taxes,
        'profits': profits,
        'buys_total': transactions_sums['buys_total'],
        'taxes_total': transactions_sums['taxes_total'],
        'profits_total': transactions_sums['profits_total'],
        'previous_total_sum': previous_total_sum,
    }
    return JsonResponse(table)
