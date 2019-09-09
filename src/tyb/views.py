from django.shortcuts import render
from django.http import HttpResponse


def current_month(request):
    return HttpResponse('Hello world!')
