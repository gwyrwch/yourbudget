import re
import logging
from datahandling.ShoppingTrip import ShoppingTrip
from algorithm.TextReader import *
import time

def only_digits(s):
    t = ''
    for c in s:
        if c.isdigit() or c == '.':
            t += c
    return float(t)


class DefaultReceiptReader:
    @classmethod
    def extract_info(cls, receipt, reader):
        extracted_data = ShoppingTrip()
        return extracted_data


class SosediReceiptReader:
    TOO_LARGE_LINE = 1.5
    CENTER_RATE_THRESHOLD = 0.5

    @classmethod
    def extract_info(cls, receipt, reader):
        from algorithm.ReceiptReader import ReceiptReader

        extracted_data = ShoppingTrip()

        extracted_data.name_of_shop = 'Соседи'
        extracted_data.address = reader(receipt.img_lines[2], lang='rus')

        avg_height = receipt.average_height

        in_shoplist = False
        i = -1

        class EnumNeeds:
            NAME = 0
            PRICE = 1

        what_we_need = EnumNeeds.NAME
        last_purchase = []

        for img_line in receipt.img_lines:
            i += 1
            center_rate = ReceiptReader.rate_center_area(img_line)
            if center_rate > cls.CENTER_RATE_THRESHOLD:
                if in_shoplist:
                    break
                in_shoplist = True
            elif in_shoplist:
                if img_line.size[1] > cls.TOO_LARGE_LINE * avg_height:
                    number_of_lines = img_line.size[1] / avg_height
                    number_of_lines = round(number_of_lines)

                    logging.info('line {} is too large. it consists of {} lines'.format(i, number_of_lines))

                    what_we_need += number_of_lines
                    what_we_need %= 2

                    last_purchase.clear()
                else:
                    last_purchase.append(img_line)
                    if what_we_need == EnumNeeds.PRICE:
                        if len(last_purchase) == 2:
                            raw_name, raw_price = last_purchase

                            # name.save('purchase_{}_name.png'.format(i))
                            # raw_price.save('purchase_{}_price.png'.format(i))
                            logging.info('created new purchase number {}'.format(i))

                            extracted_data.list_of_purchases += [(raw_name, raw_price)]
                        last_purchase.clear()
                    what_we_need = (what_we_need + 1) % 2
        extracted_data.list_of_purchases = TextReader.purchases_to_text(extracted_data.list_of_purchases, reader)
        return extracted_data


# todo: rewrite completely
class KoronaReceiptReader:
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

