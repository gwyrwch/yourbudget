from json import JSONDecoder
from datahandling.ShoppingTrip import ShoppingTrip
import requests


def decoder_fabric(cls):
    class AutoJSONDecoder(JSONDecoder):
        def __init__(self):
            def custom_object_hook(d):
                obj = cls()

                for key in d:
                    if key in obj.__dict__:
                        obj.__setattr__(key, d[key])

                return obj

            super().__init__(object_hook=custom_object_hook)
    return AutoJSONDecoder
