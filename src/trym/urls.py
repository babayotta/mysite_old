from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from trym import views
from trym.views import TransactionViewSet
#from trym.views import TransactionApi

router = routers.DefaultRouter()
router.register(r'transaction', TransactionViewSet)

app_name = 'trym'
urlpatterns = [
    path('', views.list_of_transactions, name='list_of_transactions'),
    path('change_transaction/<int:transaction_id>', views.change_transaction, name='change_transaction'),
    path('delete_transaction/<int:transaction_id>', views.delete_transaction, name='delete_transaction'),
    path('new_transaction', views.new_transaction, name='new_transaction'),
#    path('api/transactions', TransactionApi.as_view()),
#    path('api/transaction/<int:transaction_id>', TransactionApi.as_view()),
    path('api/', include(router.urls)),
    path('transaction', TemplateView.as_view(template_name='trym/home.html')),

]
