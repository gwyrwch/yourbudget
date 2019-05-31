import cv2, numpy
from PIL import Image
import logging

from algorithm.character_recognition_adapters import MeteocrAdapter
from datahandling.ShoppingTrip import Purchase
from .Meteocr import Meteocr


class TextReader:
    COUNTOURS = False

    @classmethod
    def purchases_to_text(cls, purchases, recognizer, shop_template_reader):
        logging.info('start reading text')
        result = []
        for (name, price) in purchases:
            if cls.COUNTOURS:
                price_cv2 = numpy.array(price)

                price_cv2, _ = ContourFinder.apply_contours(price_cv2)
                price = Image.fromarray(price_cv2)

            price_splitted = cls.split_into_columns(price)
            price_splitted = reversed(price_splitted)

            price = ''.join(
                cls.digit_read(single_digit_png)
                for single_digit_png in price_splitted
            )

            logging.info(price)
            price = shop_template_reader.convert_to_float(price)
            result.append(Purchase(name_of_product=recognizer.recognize(name), price=price))

        return result

    @classmethod
    def digit_read(cls, single_digit_png):
        return MeteocrAdapter().recognize(single_digit_png, Meteocr.DIGIT_CONTEXT)

    @classmethod
    def split_into_columns(cls, img):
        from algorithm.ReceiptReader import ReceiptReader
        img = img.rotate(90, expand=1, fillcolor=255)

        lines = ReceiptReader.find_unparsed_lines(img, no_rotate=True)

        lines = [
            l.rotate(-90, expand=1, fillcolor=255)
            for l in lines
        ]

        return lines


class ContourFinder:
    @classmethod
    def apply_contours(cls, im_cv2):
        contours, hierarchy = cv2.findContours(im_cv2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        areas = [
            cv2.contourArea(c)
            for c in contours
        ]

        sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)
        if not sorted_areas:
            return None

        large_contour = sorted_areas[0][1]

        im_cv2 = cv2.drawContours(im_cv2, [
            c[1]
            for c in sorted_areas[1:]
        ], -1, (0, 255, 0), 1)

        return im_cv2, large_contour
