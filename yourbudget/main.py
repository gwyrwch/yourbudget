from algorithm.ReceiptReader import ReceiptReader
# from datahandling.ShoppingTrip import ShoppingTrip
from datahandling.UserData import UserData
import os
import logging
from mongoengine import *
from datetime import datetime

TESTS_PATH = 'yourbudget/algorithm/tests/'


def test_last():
    tests = os.listdir(TESTS_PATH)
    test_path = TESTS_PATH + tests[-1]

    r = ReceiptReader.convert_to_receipt(test_path)
    exit(0)


def test_rotation():
    from PIL import Image
    path = TESTS_PATH + 'test_rotate.PNG'
    ReceiptReader.find_unparsed_lines(Image.open(path))
    exit(0)


def test_biggz():
    path = TESTS_PATH + 'test_biggz.JPG'
    r = ReceiptReader.convert_to_receipt(path)
    exit(0)


def optimize_tesseract():
    from pytesseract import image_to_string as reader, image_to_boxes
    from PIL import Image
    from algorithm.TextReader import TextReader

    test_path = TESTS_PATH + 'price.png'

    img = Image.open(test_path)

    TextReader.split_into_columns(img)

    exit(0)

def load_mongo():
    import json
    from services.AutoJsonDecoder import decoder_fabric
    from datahandling.ShoppingTrip import ShoppingTrip, Purchase
    from datahandling.ShoppingHistory import ShoppingHistory

    sh = ShoppingHistory(
        username="alex",
        all_trips=[
            ShoppingTrip(
                name_of_shop="Корона",
                trip_date=datetime.fromisoformat("2019-04-20"),
                receipt_amount=102.87,
                address="Пр. Победителей 11",
                receipt_discount=8,
                category="Grocery",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=0.87
                    ),
                    Purchase(
                        name_of_product="Bar",
                        price=102
                    )
                ]
            ),
            ShoppingTrip(
                name_of_shop="Пятый элемент",
                trip_date=datetime.fromisoformat("2019-04-17"),
                receipt_amount=500,
                address="Пр. Победителей 22",
                receipt_discount=0,
                category="Electronics",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=500
                    ),
                ]
            ),
            ShoppingTrip(
                name_of_shop="Соседи",
                trip_date=datetime.fromisoformat("2019-04-17"),
                receipt_amount=128,
                address="Пр. Победителей 49",
                receipt_discount=0,
                category="Grocery",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=128
                    ),
                ]
            ),
            ShoppingTrip(
                name_of_shop="Mcdonald's",
                trip_date=datetime.fromisoformat("2019-02-17"),
                receipt_amount=10,
                address="Бобруйская 6",
                receipt_discount=0,
                category="Food",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=10
                    ),
                ]
            ),
            ShoppingTrip(
                name_of_shop="Bershka",
                trip_date=datetime.fromisoformat("2019-02-17"),
                receipt_amount=100,
                address="Независимости 85",
                receipt_discount=0,
                category="Clothes",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=100
                    ),
                ]
            ),
            ShoppingTrip(
                name_of_shop="Корона",
                trip_date=datetime.fromisoformat("2019-02-20"),
                receipt_amount=77.01,
                address="Пр. Победителей 11",
                receipt_discount=8,
                category="Grocery",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=1
                    ),
                    Purchase(
                        name_of_product="Bar",
                        price=76.01
                    )
                ]
            ),
            ShoppingTrip(
                name_of_shop="Пятый элемент",
                trip_date=datetime.fromisoformat("2019-03-17"),
                receipt_amount=200,
                address="Пр. Победителей 22",
                receipt_discount=0,
                category="Electronics",
                list_of_purchases=[
                    Purchase(
                        name_of_product="Foo",
                        price=200
                    ),
                ]
            ),
        ]
    )

    connect('myNewDatabase')

    # sh.save()

if __name__ == '__main__':
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    load_mongo()
    # optimize_tesseract()
    # test_last()


