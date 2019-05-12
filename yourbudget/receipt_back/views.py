from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.views import View

from datahandling.UserData import UserData
from receipt_back.models import User
from services import get_percent, get_relative_percent, move_date_back, get_date

from datetime import date

import logging


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
    
    today = get_date(date.today())
    
    # fixme:gitt  delete
    today = move_date_back(today, cnt_month=1)
    
    month_ago = move_date_back(today, cnt_month=1)

    spent_on_fav_product_this_month = history.get_amount_spent_on_fav_product(
        current_user.fav_product,
        *today
    )
    spent_on_fav_product_last_month = history.get_amount_spent_on_fav_product(
        current_user.fav_product,
        *month_ago
    )
    fav_product_percent, fav_product_annotation = get_relative_percent(
        spent_on_fav_product_this_month, spent_on_fav_product_last_month
    )

    average_receipt_this_month = history.get_average_receipt(
        *today
    )
    average_receipt_last_month = history.get_average_receipt(
        *month_ago
    )
    average_receipt_percent, average_receipt_annotation = get_relative_percent(
        average_receipt_this_month, average_receipt_last_month
    )

    trips_this_month = history.get_number_of_trips(
        *today
    )
    trips_last_month = history.get_number_of_trips(
        *month_ago
    )
    trips_percent, trips_annotation = get_relative_percent(
        trips_this_month, trips_last_month
    )

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
                'all_purchases_percent': get_percent(all_purchases),

                'fav_product': current_user.fav_product,
                'spent_on_fav_product': spent_on_fav_product_this_month,
                'fav_product_percent': fav_product_percent,
                'fav_product_annotation': fav_product_annotation,

                'average_receipt': average_receipt_this_month,
                'average_receipt_annotation': average_receipt_annotation,
                'average_receipt_percent': average_receipt_percent,

                'number_of_trips': trips_this_month,
                'number_of_trips_annotation': trips_annotation,
                'number_of_trips_percent': trips_percent
            }
        }
    )


def alltrips(request):
    current_user = request.user
    if current_user is None or not current_user.is_authenticated:
        return HttpResponseRedirect(redirect_to='login')

    return render(request, 'alltrips.html', context={
        'full_name': current_user.get_full_name(),
    })


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
        print(result)
        first_name = result.get('first-name')
        last_name = result.get('last-name')
        gender = result.get('gender')
        print(gender)
        date_of_birth = result.get('date-of-birth')
        username = result.get('username')
        email = result.get('email')
        city = result.get('city')
        country = result.get('country')
        telegram_username = result.get('telegram_username')

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
                city=city,
                telegram_username=telegram_username
            )

            return HttpResponseRedirect(redirect_to='login')
        except ValueError as e:
            # Value error in create_user(), or passwords dont match
            logging.info(str(e))

            a = HttpResponse()
            a.status_code = 400
            return a
        except IntegrityError as e:
            logging.info(str(e))

            # Duplicate
            a = HttpResponse()
            a.status_code = 402
            return a
        except ValidationError as e:
            # Bad password
            logging.info(str(e))

            a = HttpResponse()
            a.status_code = 401
            return a


class SettingsView(View):
    def get(self, request):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect(redirect_to='login')

        return render(request, 'settings.html', context={
            'full_name': current_user.get_full_name(),
            'email': current_user.email,
            'firstname': current_user.first_name,
            'lastname': current_user.last_name,
            'telegram_username': current_user.telegram_username,
            'fav_product': current_user.fav_product,
            'male_checked': 'checked' if current_user.gender == 'male' else '',
            'female_checked': 'checked' if current_user.gender == 'female' else '',

        })

    def post(self, request):
        current_user = request.user

        if not current_user.is_authenticated:
            return HttpResponseRedirect(redirect_to='login')

        result = request.POST
        settings = result.get('settings')

        if settings == 'general':
            gender = result.get('gender')
            if gender:
                current_user.gender = gender
            first_name = result.get('firstname')
            if first_name:
                current_user.first_name = first_name
            last_name = result.get('lastname')
            if last_name:
                current_user.last_name = last_name
            email = result.get('email')
            if email:
                current_user.email = email
            telegram_username = result.get('telegram_username')
            if telegram_username:
                current_user.telegram_username = telegram_username

            current_user.save()

            return HttpResponseRedirect('settings')
        elif settings == 'preferences':
            fav_product = result.get('fav_product')
            if fav_product:
                current_user.fav_product = fav_product
            current_user.save()
            return HttpResponseRedirect('settings')
        elif settings == 'password':
            old_password = result.get('old_password')
            password1 = result.get('password1')
            password2 = result.get('password2')

            temp_user = authenticate(username=current_user.username, password=old_password)

            if old_password and password1 and password2:
                if temp_user is None or password1 != password2:
                    return HttpResponseBadRequest()
                current_user.set_password(password1)
                current_user.save()

                login(request, current_user)

            return HttpResponseRedirect('settings')
        else:
            return HttpResponseBadRequest()
