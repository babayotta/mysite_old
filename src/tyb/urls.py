from django.urls import path
from tyb import views

app_name = 'tyb'
urlpatterns = [
    path('', views.current_month, name='current_month'),
    path('api', views.tyb_api, name='tyb_api'),
]
