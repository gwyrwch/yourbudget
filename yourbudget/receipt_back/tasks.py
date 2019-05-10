import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from datahandling.UserData import UserData
from yourbudget.celery import app
from algorithm.ReceiptReader import ReceiptReader
import os


@app.task
def save_trip(username, img_path):
    logging.info('saving trip for {0} from {1}'.format(username, img_path))

    shopping_trip = ReceiptReader.convert_to_receipt(img_path)

    logging.info('finished parsing')

    from mongoengine import connect
    connect('myNewDatabase')

    history = UserData.get_history( username)
    history.all_trips.append(shopping_trip)
    history.save()

    os.remove(img_path)
