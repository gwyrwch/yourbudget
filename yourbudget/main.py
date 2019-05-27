from algorithm.ReceiptReader import ReceiptReader
# from datahandling.ShoppingTrip import ShoppingTrip
from datahandling.UserData import UserData
import os
import logging
from mongoengine import *
from algorithm.TextReader import TextReader
from pytesseract import image_to_string as reader
from algorithm.readers import SosediReceiptReader
from PIL import Image

from training import prepare_samples, process_samples, main_training, test_meteocr

TESTS_PATH = 'yourbudget/algorithm/tests/'


def test_last():
    tests = os.listdir(TESTS_PATH)
    test_path = TESTS_PATH + 'test_sosedi.JPG'

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
    
def test_updated_algotihm():
    ReceiptReader.convert_to_receipt(TESTS_PATH + 'test_sosedi.JPG')

    # tt = TextReader.purchases_to_text([
    #     (Image.open('yourbudget/result_lines/purchase_47_name.png'), Image.open('yourbudget/result_lines/purchase_47_price.png'))
    # ], reader, SosediReceiptReader)
    # print(tt[0].name_of_product)



if __name__ == '__main__':
    # connect('myNewDatabase')

    test_last()
    # prepare_samples(TESTS_PATH)
    # main_training()
    # test_meteocr(TESTS_PATH, verbose=False)
