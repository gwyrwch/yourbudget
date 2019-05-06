from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from datahandling.UserData import UserData
from receipt_back.models import User
from PIL import Image
import io, random, string


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

        try:
            user = User.objects.get(telegram_username=telegram_username)
        except User.DoesNotExist:
            return HttpResponse(b'User with such telegram username wasnt found.', status=401)

        image = Image.open(io.BytesIO(photo_in_bytes))

        filename = filename.replace('/', '')
        img_path = user.username + '-' + filename
        image.save(img_path)

        return HttpResponse()
