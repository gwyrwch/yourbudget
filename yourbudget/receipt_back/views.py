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
        username_or_email = result.get('usernameOrEmail')
        password = result.get('password')
        remember_me = result.get('rememberMe')

        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to='index')
        else:
            a = HttpResponse()
            a.status_code = 400
            return a


class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        result = request.POST
        first_name = result.get('first-name')
        last_name = result.get('last-name')
        gender = result.get('gender')
        date_of_birth = result.get('date-of-birth')
        username = result.get('username')
        email = result.get('email')
        city = result.get('city')
        country = result.get('country')

        try:
            user = User.objects.create_user(
                username,
                email,
                password='',
                # password1 password2
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=date_of_birth,
                country=country,
                city=city
            )
            return HttpResponseRedirect(redirect_to='login')
        except:
            a = HttpResponse()
            a.status_code = 400
            return a


