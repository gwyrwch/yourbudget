import re
import logging
from datahandling.ShoppingTrip import ShoppingTrip, Purchase
from algorithm.TextReader import TextReader, ContourFinder
import time
import datetime


def only_digits(s):
    t = ''
    no_dots = True
    for c in s:
        if c.isdigit():
            t += c
        elif c == '.' and no_dots:
            t += c
            no_dots = False
    return float(t)


class DefaultReceiptReader:
    @classmethod
    def convert_to_float(cls, raw_price):
        return 0

    @classmethod
    def extract_info(cls, receipt, reader):
        """
        Reads special type of

        :param img
            PIL gray image

        :returns
            compressed image
        """
        extracted_data = ShoppingTrip()
        return extracted_data


class SosediReceiptReader:
    TOO_LARGE_LINE = 1.5
    CENTER_RATE_THRESHOLD = 0.4

    @classmethod
    def convert_to_float(cls, raw_price):
        # template looks like: =0.59*1.000$0.59
        if '$' not in raw_price:
            pos_star = raw_price.find('*')
            if pos_star != -1:
                return only_digits(raw_price[0:pos_star])
            return 0
        l, r = raw_price.rsplit('$', 1)
        return only_digits(r)

    @classmethod
    def extract_info(cls, receipt, reader):
        from algorithm.ReceiptReader import ReceiptReader

        extracted_data = ShoppingTrip()

        extracted_data.name_of_shop = 'Соседи'
        extracted_data.address = reader(receipt.img_lines[2], lang='rus')
        extracted_data.trip_date = datetime.datetime.now()

        list_of_purchases = []

        avg_height = receipt.average_height

        in_shoplist = False

        class EnumNeeds:
            NAME = 0
            PRICE = 1

        what_we_need = EnumNeeds.NAME
        last_purchase = []

        for img_line, i in zip(receipt.img_lines, range(len(receipt.img_lines))):
            center_rate = ReceiptReader.rate_center_area(img_line)
            if center_rate > cls.CENTER_RATE_THRESHOLD:
                if in_shoplist:
                    logging.info('finished shopping')
                    break
                in_shoplist = True
                logging.info('starting shopping')
            elif in_shoplist:
                if img_line.size[1] > cls.TOO_LARGE_LINE * avg_height:
                    number_of_lines = img_line.size[1] / avg_height
                    number_of_lines = int(number_of_lines + 0.5)

                    logging.info('line {} is too large. it consists of {} lines'.format(i, number_of_lines))

                    what_we_need += number_of_lines
                    what_we_need %= 2

                    last_purchase.clear()
                else:
                    last_purchase.append(img_line)
                    if what_we_need == EnumNeeds.PRICE:
                        if len(last_purchase) == 2:
                            raw_name, raw_price = last_purchase

                            raw_name.save('result_lines/purchase_{}_name.png'.format(i))
                            raw_price.save('result_lines/purchase_{}_price.png'.format(i))

                            logging.info('created new purchase number {}'.format(i))

                            list_of_purchases += [(raw_name, raw_price)]
                        last_purchase.clear()
                    what_we_need = (what_we_need + 1) % 2
        logging.info('Total num of puurchases is {}'.format(len(list_of_purchases)))
        extracted_data.list_of_purchases = TextReader.purchases_to_text(list_of_purchases, reader, cls)
        extracted_data.receipt_amount = sum(
            [
                purchase.price
                for purchase in extracted_data.list_of_purchases
             ]
        )
        return extracted_data


# todo: rewrite completely
class KoronaReceiptReader:
    @classmethod
    def convert_to_float(cls, raw_price):
        return 0

    @classmethod
    def extract_info(cls, receipt, reader):
        extracted_data = ShoppingTrip()

        return extracted_data

    @classmethod
    def find_data(cls, text):
        for line in text:
            data = re.search(r'[0-9]{0,2}[-:.][0-9]{0,2}[-:.][0-9]{0,4}', line)
            if data and '2019' in data.group():
                return data.group()
        return None

