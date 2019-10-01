import datetime
from calendar import monthrange
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Q, Value as V
from django.db.models.functions import Coalesce
from tyb.models import Transaction


def current_month(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')

    return render(request, 'tyb/current_month.html', {})


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
            'transactions': [{
                'pk': transaction.pk,
                'description': transaction.description,
                'cash': transaction.cash,
            } for transaction in buy_transactions_for_day],
            'budget_for_day': budget_for_days[day],
            'balance_for_day': balance_for_previous_day,
        })
        if tax_transactions_for_day:
            taxes.append({
                'date': date,
                'transactions': [{
                    'pk': transaction.pk,
                    'description': transaction.description,
                    'cash': transaction.cash,
                } for transaction in tax_transactions_for_day],
            })
        if profit_transactions_for_day:
            profits.append({
                'date': date,
                'transactions': [{
                    'pk': transaction.pk,
                    'description': transaction.description,
                    'cash': transaction.cash,
                } for transaction in profit_transactions_for_day],
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
