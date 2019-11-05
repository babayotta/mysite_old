from django.urls import path
from trym import views
from trym.views import TransactionApi

app_name = 'trym'
urlpatterns = [
    path('', views.list_of_transactions, name='list_of_transactions'),
    path('change_transaction/<int:transaction_id>', views.change_transaction, name='change_transaction'),
    path('delete_transaction/<int:transaction_id>', views.delete_transaction, name='delete_transaction'),
    path('new_transaction', views.new_transaction, name='new_transaction'),
    path('api/transactions', TransactionApi.as_view()),
    path('api/transaction/<int:transaction_id>', TransactionApi.as_view()),
]
