from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.views import View

from datahandling.UserData import UserData
from receipt_back.models import User
from services import get_percent


def index(request):
    from mongoengine import connect
    connect('myNewDatabase')

    current_user = request.user
    if current_user is None or not current_user.is_authenticated:
        return HttpResponseRedirect(redirect_to='login')

    history = UserData.get_history(current_user.username)

    registered_shopping_trips = len(history.all_trips)
    total_spend_amount = sum(trip.receipt_amount for trip in history.all_trips)
    total_discount = sum(trip.receipt_discount for trip in history.all_trips)
    all_purchases = sum(len(trip.list_of_purchases) for trip in history.all_trips)

    return render(
        request, 'index.html', context={
            'full_name': current_user.get_full_name(),
            'top3': history.top_three(),
            'progress_bar_data': {
                'registered_shopping_trips': registered_shopping_trips,
                'registered_shopping_trips_percent': get_percent(registered_shopping_trips),
                'total_spend_amount': total_spend_amount,
                'total_spend_amount_percent': get_percent(total_spend_amount),
                'total_discount': total_discount,
                'total_discount_percent': get_percent(total_discount),
                'all_purchases': all_purchases,
                'all_purchases_percent': get_percent(all_purchases)
            }
        }
    )


def not_found(request, exception):
    return render(request, '404.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to='login')


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


def get_current_data(request):
    current_user = request.user
    chart = request.GET.get('chart')

    if not current_user.is_authenticated:
        return HttpResponseBadRequest()

    history = UserData.get_history(current_user.username)

    if chart == 'overview':
        overview, top_three = history.get_data_for_overview()
        return JsonResponse({
            'overview': overview,
            'top3': top_three
        })
    elif chart == 'categorization':
        categorization = history.get_data_for_categorization()
        return JsonResponse(
            # categorization
            [
            {"label": "Grocery", "value": 62},
            {"label": "Clothes", "value": 29},
            {"label": "Food", "value": 5},
            {"label": "Electronics", "value": 4},
        ], safe=False)
    else:
        return HttpResponseBadRequest()
