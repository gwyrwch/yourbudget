from django.urls import path

from . import views

urlpatterns = [
    path('<str:link>', views.index, name='index'),
]