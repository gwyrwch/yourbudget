class ShoppingTrip:
    def __init__(self):
        self.name_of_shop = None
        self.trip_date = None
        self.receipt_amount = None
        self.receipt_discount = None
        self.list_of_purchases = []

    def _json(self):
        return {
            'name_of_shop': self.name_of_shop,
            'trip_date': self.trip_date,
            'receipt_amount': self.receipt_amount,
            'receipt_discount': self.receipt_discount,
            'list_of_purchases': self.list_of_purchases
        }

    def __str__(self):
        d = {
            'Название': self.name_of_shop,
            'Дата': self.trip_date,
            'Сумма в чеке': self.receipt_amount,
            'Скидка': self.receipt_discount,
            'Список покупок': self.list_of_purchases
        }

        s = ''

        for k in d:
            s += k + ': ' + str(d[k]) + '\n'

        return s



