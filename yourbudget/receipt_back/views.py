from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User


def index(request):
    current_user = request.user
    if current_user is None or not current_user.is_authenticated:
        return HttpResponseRedirect(redirect_to='login')
    return render(
        request, 'index.html', context={
            'full_name': current_user.get_full_name()
        }
    )


def not_found(request, exception):
    return render(request, '404.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        result = request.POST
        usernameOrEmail = result.get('usernameOrEmail')
        password = result.get('password')
        rememberMe = result.get('rememberMe')

        user = authenticate(request, username=usernameOrEmail, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to='index')
        else:
            a = HttpResponse()
            a.status_code = 400
            return a
