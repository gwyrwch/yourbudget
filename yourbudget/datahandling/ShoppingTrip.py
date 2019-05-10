import json
import mongoengine


class Purchase(mongoengine.EmbeddedDocument):
    name_of_product = mongoengine.StringField(default='')
    price = mongoengine.FloatField(default=0)


class ShoppingTrip(mongoengine.EmbeddedDocument):
    name_of_shop = mongoengine.StringField(default='')
    trip_date = mongoengine.DateField()
    receipt_amount = mongoengine.FloatField(default=0)
    receipt_discount = mongoengine.FloatField(default=0)
    address = mongoengine.StringField(default='')
    category = mongoengine.StringField(default='')
    list_of_purchases = mongoengine.EmbeddedDocumentListField(Purchase, default=[])

    def _json(self):
        return {
            'name_of_shop': self.name_of_shop,
            'trip_date': self.date_to_string(self.trip_date),
            'receipt_amount': str(self.receipt_amount),
            'receipt_discount': str(self.receipt_discount),
            'list_of_purchases': [
                {
                    'price': p.price,
                    'name_of_product': p.name_of_product
                }
                for p in self.list_of_purchases
            ],
            'category': self.category,
            'address':  self.address
        }

    @staticmethod
    def date_to_string(date):
        if date is None:
            return ''
        return '{}/{}/{}'.format(date.day, date.month, date.year)

    def get_data_for_table(self):
        return self._json()

    def __str__(self):
        d = {
            u'Название': self.name_of_shop,
            u'Дата': self.trip_date,
            u'Сумма в чеке': self.receipt_amount,
            u'Скидка': self.receipt_discount,
            u'Список покупок': self.list_of_purchases,
            u'Категория': self.category,
            u'Адрес': self.address
        }

        return json.dumps(d, ensure_ascii=False)

