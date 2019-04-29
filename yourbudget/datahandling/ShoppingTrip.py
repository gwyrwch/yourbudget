import json

class ShoppingTrip:
    def __init__(self):
        self.name_of_shop = None
        self.trip_date = None
        self.receipt_amount = None
        self.receipt_discount = None
        self.address = None
        self.list_of_purchases = []

    def _json(self):
        return {
            'name_of_shop': self.name_of_shop,
            'trip_date': self.trip_date,
            'receipt_amount': self.receipt_amount,
            'receipt_discount': self.receipt_discount,
            'list_of_purchases': self.list_of_purchases,
            'address':  self.address
        }

    def __str__(self):
        d = {
            u'Название': self.name_of_shop,
            u'Дата': self.trip_date,
            u'Сумма в чеке': self.receipt_amount,
            u'Скидка': self.receipt_discount,
            u'Список покупок': self.list_of_purchases,
            u'Адрес': self.address
        }

        return json.dumps(d, ensure_ascii=False)


