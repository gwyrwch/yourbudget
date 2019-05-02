from django.urls import path

from . import views

handler404 = 'receipt_back.views.not_found'

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('registration', views.RegistrationView.as_view(), name='registration_view')
]
