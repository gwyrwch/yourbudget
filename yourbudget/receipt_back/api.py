import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from datahandling.ShoppingTrip import ShoppingTrip
from datahandling.UserData import UserData
from receipt_back.models import User
from PIL import Image
import io, random, string

from receipt_back.tasks import save_trip


def get_current_data(request):
    """
    Searches for data to display on the charts.
    :param request:
    :return: Json of morris chart data
    """
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
        # TODO
        return JsonResponse(categorization, safe=False)
    else:
        return HttpResponseBadRequest()


def get_all_trips_data(request):
    from mongoengine import connect
    connect('myNewDatabase')

    current_user = request.user

    if not current_user.is_authenticated:
        return HttpResponseBadRequest()

    history = UserData.get_history(current_user.username)

    resp = JsonResponse({
        'data': [
            trip.get_data_for_table()
            for trip in history.all_trips
        ]
    })

    return resp


class Telegram:
    @staticmethod
    @csrf_exempt
    def save_receipt(request):
        if request.method != 'POST':
            return HttpResponseBadRequest(b'Wrong method')

        files = request.FILES

        if len(files) != 1:
            return HttpResponseBadRequest(b"A single file must be send.")

        # files has a single key, value pair
        filename, photo_in_bytes = list(files.items())[0]
        photo_in_bytes = photo_in_bytes.read()

        telegram_username = request.POST['telegram_username']
        save = request.POST.get('save')

        try:
            user = User.objects.get(telegram_username=telegram_username)
        except User.DoesNotExist:
            return HttpResponse(b'User with such telegram username wasnt found.', status=401)

        image = Image.open(io.BytesIO(photo_in_bytes))

        filename = filename.replace('/', '')
        img_path = user.username + '-' + filename
        image.save(img_path)

        try:
            save_trip.delay(user.username, img_path, save)
        except:
            return HttpResponse(b'Service temporary unavaiable', status=500)

        return HttpResponse(status=200)

    @staticmethod
    @csrf_exempt
    def save_trip_manual(request):
        from mongoengine import connect
        connect('myNewDatabase')

        if request.method != 'POST':
            return HttpResponseBadRequest(b'Wrong method')

        raw_body = request.body
        result = json.loads(raw_body)

        telegram_username = result['telegram_username']
        raw_shopping_trip = result['trip']

        try:
            user = User.objects.get(telegram_username=telegram_username)
        except User.DoesNotExist:
            return HttpResponse(b'User with such telegram username wasnt found.', status=401)

        shopping_trip = ShoppingTrip._from_son(raw_shopping_trip)

        history = UserData.get_history(user.username)
        history.all_trips.append(shopping_trip)
        history.save()

        return HttpResponse(status=200)
