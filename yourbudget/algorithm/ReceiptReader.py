from PIL import Image

from algorithm.Receipt import Receipt
import cv2

import pyocr
import pyocr.builders
import pytesseract

USE_PYOCR = False
USE_UPDATE = False

def cut_noise(image):
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')

class ReceiptReader:
    @classmethod
    def preetify_token(cls, t):
        # todo: научится пользоваться
        if t == u'КИДКА':
            return 'СКИДКА'

        return t

    @classmethod
    def preetify_line(cls, s):
        tokens = s.split()

        tokens = [
            cls.preetify_token(t)
            for t in tokens
        ]

        return ' '.join(
            tokens
        )

    @classmethod
    def convert_to_receipt(cls, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)

        if USE_PYOCR:
            tools = pyocr.get_available_tools()

            tool = tools[0]

            img = Image.open(image_path)
            img = img.convert("L")
            img = cut_noise(img)

            text = tool.image_to_string(img, lang='rus')
        elif USE_UPDATE:
            text = pytesseract.image_to_string(Image.open(filename), lang='rus')
        else:
            text = pytesseract.image_to_string(Image.open(image_path), lang='rus')


        lines = text.splitlines()

        lines = [
            cls.preetify_line(s)
            for s in lines
        ]

        lines = [s for s in lines if len(s) > 0]

        return Receipt(lines)
