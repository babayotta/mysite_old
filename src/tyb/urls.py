from django.urls import path
from tyb import views

app_name = 'tyb'
urlpatterns = [
    path('', views.list_of_transactions, name='list_of_transactions'),
    path('<int:transaction_id>/', views.change_transaction, name='change_transaction'),
]
