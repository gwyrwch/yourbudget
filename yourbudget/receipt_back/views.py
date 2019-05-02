from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from receipt_back.models import User


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to='login')


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

        password1 = result.get('password1')
        password2 = result.get('password2')

        try:
            if password1 != password2:
                raise ValueError("Passwords don't match")

            password = password1
            validate_password(password)

            user = User.objects.create_user(
                username,
                email,
                password,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=date_of_birth,
                country=country,
                city=city
            )

            return HttpResponseRedirect(redirect_to='login')
        except (ValueError, ):
            # Value error in create_user(), or passwords dont match

            a = HttpResponse()
            a.status_code = 400
            return a
        except IntegrityError:
            # Duplicate
            a = HttpResponse()
            a.status_code = 402
            return a
        except ValidationError:
            # Bad password
            a = HttpResponse()
            a.status_code = 401
            return a



