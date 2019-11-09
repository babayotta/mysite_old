import datetime
from calendar import monthrange
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q, Value as V
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from trym.serializers import TransactionSerializer
from trym.models import Transaction
from trym.forms import TransactionForm


def list_of_transactions(request):
    if not request.user.is_authenticated:
        return render(request, 'mysite/home.html')

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
        profits_total=Coalesce(Sum('value', filter=Q(transaction_type=Transaction.PROFIT)), V(0)),
        taxes_total=Coalesce(Sum('value', filter=Q(transaction_type=Transaction.TAX)), V(0)),
        buys_total=Coalesce(Sum('value', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )

    previous_total_sum = Transaction.objects.filter(user=user, date__lt=today.replace(day=1)).aggregate(
        value=
        Coalesce(Sum('value', filter=Q(transaction_type=Transaction.PROFIT)), V(0)) -
        Coalesce(Sum('value', filter=Q(transaction_type=Transaction.TAX)), V(0)) -
        Coalesce(Sum('value', filter=Q(transaction_type=Transaction.BUY)), V(0))
    )['value']

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
                sum_buy_for_day += transaction.value
                buy_transactions_for_day.append(transaction)
        for transaction in tax_transactions:
            if transaction.date == date:
                sum_tax_for_day += transaction.value
                tax_transactions_for_day.append(transaction)
        for transaction in profit_transactions:
            if transaction.date == date:
                sum_profit_for_day += transaction.value
                profit_transactions_for_day.append(transaction)

        budget_for_day = (sum_profit_for_day - sum_tax_for_day + balance_for_previous_day) / remaining_days
        for i in range(day, number_of_days):
            budget_for_days[i] += budget_for_day
        balance_for_previous_day = budget_for_days[day] - sum_buy_for_day
        remaining_days -= 1

        buys.append({
            'date': date,
            'transactions': [{
                'id': transaction.id,
                'description': transaction.description,
                'value': transaction.value,
            } for transaction in buy_transactions_for_day],
            'budget_for_day': round(budget_for_days[day], 2),
            'balance_for_day': round(balance_for_previous_day, 2),
        })
        if tax_transactions_for_day:
            taxes.append({
                'date': date,
                'transactions': [{
                    'id': transaction.id,
                    'description': transaction.description,
                    'value': transaction.value,
                } for transaction in tax_transactions_for_day],
            })
        if profit_transactions_for_day:
            profits.append({
                'date': date,
                'transactions': [{
                    'id': transaction.id,
                    'description': transaction.description,
                    'value': transaction.value,
                } for transaction in profit_transactions_for_day],
            })

    table = {
        'buys': buys,
        'taxes': taxes,
        'profits': profits,
        'buys_total': round(transactions_sums['buys_total'], 2),
        'taxes_total': round(transactions_sums['taxes_total'], 2),
        'profits_total': round(transactions_sums['profits_total'], 2),
        'previous_total_sum': round(previous_total_sum, 2),
    }

    return render(request, 'trym/list_of_transactions.html', table)


def change_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return list_of_transactions(request)
        else:
            print(form.errors)
    else:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        form = TransactionForm(initial={
            'date': transaction.date,
            'transaction_type': transaction.transaction_type,
            'description': transaction.description,
        }, instance=transaction)
    return render(request, 'trym/transaction.html', {'form': form, 'action_url': request.path})


def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return list_of_transactions(request)
        else:
            print(form.errors)
    else:
        form = TransactionForm
    return render(request, 'trym/transaction.html', {'form': form, 'action_url': request.path})


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return list_of_transactions(request)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = {
        'id': ['exact', 'lte', 'gte', ],
        'date': ['exact', 'lte', 'gte', ],
        'transaction_type': ['exact', ],
    }

#class TransactionApi(APIView):
#    def get(self, request):
#        today = datetime.date.today()
#        user = request.user
#        transactions = Transaction.objects.filter(user=user,
#                                                  date__year=today.year,
#                                                  date__month=today.month)
#        serializer = TransactionSerializer(transactions, many=True)
#        return Response({'transactions': serializer.data})
#
#    def post(self, request):
#        user = request.user
#        transaction = request.data.get('transaction')
#        transaction['user_id'] = user.id
#
#        serializer = TransactionSerializer(data=transaction)
#        if serializer.is_valid(raise_exception=True):
#            transaction_saved = serializer.save()
#            return Response({
#                'success': 'Transaction "{}" created successfully'.format(transaction_saved.description)
#            })
#
#    def put(self, request, transaction_id):
#        user = request.user
#        saved_transaction = get_object_or_404(Transaction.objects.filter(user=user), id=transaction_id)
#        data = request.data.get('transaction')
#        serializer = TransactionSerializer(instance=saved_transaction, data=data, partial=True)
#
#        if serializer.is_valid(raise_exception=True):
#            transaction_saved = serializer.save()
#            return Response({
#                "success": "Transaction '{}' updated successfully".format(transaction_saved.description)
#            })
#
#    def delete(self, request, transaction_id):
#        user = request.user
#        transaction = get_object_or_404(Transaction.objects.filter(user=user), id=transaction_id)
#        transaction.delete()
#        return Response({
#            "message": "Transaction with id `{}` has been deleted.".format(transaction_id)
#        }, status=204)
