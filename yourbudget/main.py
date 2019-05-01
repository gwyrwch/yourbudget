from algorithm.ReceiptReader import ReceiptReader
from datahandling.User import User
import os
import logging

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


if __name__ == '__main__':
    logging.basicConfig(filename="sample.log", level=logging.INFO)

    # optimize_tesseract()
    test_last()


