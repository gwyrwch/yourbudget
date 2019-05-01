from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def not_found(request, exception):
    return render(request, '404.html')
