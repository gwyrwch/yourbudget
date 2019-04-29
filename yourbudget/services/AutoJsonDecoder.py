from json import JSONDecoder
from datahandling.ShoppingTrip import ShoppingTrip
import requests


def custom_object_hook(d):
    trip_obj = ShoppingTrip()
    trip_obj.list_of_purchases = d['list_of_purchases']
    trip_obj.receipt_discount = d['receipt_discount']
    trip_obj.receipt_amount = d['receipt_amount']
    trip_obj.trip_date = d['trip_date']
    trip_obj.name_of_shop = d['name_of_shop']
    trip_obj.address = d['address']
    return trip_obj


class AutoJSONDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=custom_object_hook)
