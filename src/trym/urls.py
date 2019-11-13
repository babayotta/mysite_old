from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from trym.views import TransactionViewSet

router = routers.DefaultRouter()
router.register(r'transaction', TransactionViewSet)

app_name = 'trym'
urlpatterns = [
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='trym/home.html'), name="home"),
]
