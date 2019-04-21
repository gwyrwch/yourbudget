import re
from datahandling.ShoppingTrip import ShoppingTrip


def only_digits(s):
    t = ''
    for c in s:
        if c.isdigit() or c == '.':
            t += c
    return float(t)

class KoronaReceiptParser:
    @classmethod
    def extract_info(cls, receipt):
        extracted_data = ShoppingTrip()
        extracted_data.name_of_shop = 'Корона'
        extracted_data.trip_date = KoronaReceiptParser.find_data(receipt.info)
        extracted_data.receipt_discount = KoronaReceiptParser.find_discount(receipt.info)
        extracted_data.receipt_amount = KoronaReceiptParser.find_amount(receipt.info)

        for i in range(len(receipt.info)):
            if receipt.info[i].count('=') and receipt.info[i].count(u'х'):
                try:
                    name = receipt.info[i - 1]
                    print(receipt.info[i])
                    price, amount = map(only_digits, receipt.info[i].split()[1:3])

                    print(name)
                    print(price, amount)

                    extracted_data.list_of_purchases.append(
                        (name, price * amount)
                    )
                except:
                    pass
            elif receipt.info[i].count('=') == 2:
                try:
                    name = receipt.info[i - 1]
                    raw_price = receipt.info[i].split()[-1][1:]

                    extracted_data.list_of_purchases.append(
                        (name, only_digits(raw_price))
                    )
                except:
                    pass



        return extracted_data

    @classmethod
    def find_data(cls, text):
        for line in text:
            data = re.search(r'[0-9]{0,2}[-:.][0-9]{0,2}[-:.][0-9]{0,4}', line)
            if data and '2019' in data.group():
                return data.group()
        return None

    @classmethod
    def find_discount(cls, text):
        for line in text:
            discount = re.search(r'ИТОГО СКИДКА', line)
            if discount:
                print(discount)
                return discount.group()
        return None

    @classmethod
    def find_amount(cls, text):
        for line in text:
            amount = re.search(r'ИТОГО К ОПЛАТЕ', line)
            if amount:
                return amount.group()

        return None
