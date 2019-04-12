from django.shortcuts import render
from django.http import HttpResponse


def index(request, link):

    return HttpResponse("Hello, world. You're at the receipt index. {}".format(link))
