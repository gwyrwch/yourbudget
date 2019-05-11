import itertools
from datetime import datetime
import mongoengine
from datahandling.ShoppingTrip import ShoppingTrip
from services import move_date_back, get_date

map_month = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'June',
      'July',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
]


class ShoppingHistory(mongoengine.Document):
    username = mongoengine.StringField(primary_key=True)
    all_trips = mongoengine.EmbeddedDocumentListField(ShoppingTrip, default=[])

    def top_three(self):
        trips = sorted(self.all_trips, key=lambda x: x.name_of_shop)
        grouped = itertools.groupby(
            trips, key=lambda x: x.name_of_shop
        )

        result = []
        for k, v in grouped:
            result.append(
                (
                    sum(
                        trip.receipt_amount
                        for trip in v
                    ), k
                )
            )

        result.sort(reverse=True)
        default_shops = [(0, u'Красти Краб'), (0, u'Чам Баккет'), (0, u'Кинотеатр «Риф»')]
        result += default_shops

        return [
            result[i][1]
            for i in range(3)
        ]

    def get_data_for_overview(self):
        trips = filter(lambda x: x.trip_date, self.all_trips)
        trips = sorted(trips, key=lambda x: get_date(x.trip_date))

        if len(trips) == 0:
            today = datetime.today()
            last_receipt_date = (today.year, today.month)
        else:
            last_receipt_date = get_date(trips[-1].trip_date)

        grouped = itertools.groupby(
            trips, key=lambda x: get_date(x.trip_date)
        )

        six_month_earlier = move_date_back(last_receipt_date, 6)

        top_three = self.top_three()

        dates_in_chart = set()
        ans = []

        for k, v in grouped:
            if k <= six_month_earlier:
                continue

            dates_in_chart.add(k)

            v = list(v)
            ans.append({
                'y': k,
                'a': str(
                    sum(
                        trip.receipt_amount
                        for trip in filter(lambda x: x.name_of_shop == top_three[0], v)
                    )
                ),
                'b': str(
                    sum(
                        trip.receipt_amount
                        for trip in filter(lambda x: x.name_of_shop == top_three[1], v)
                    )
                ),
                'c': str(
                    sum(
                        trip.receipt_amount
                        for trip in filter(lambda x: x.name_of_shop == top_three[2], v)
                    )
                ),
            })

        i = last_receipt_date
        while i > six_month_earlier:
            if i not in dates_in_chart:
                ans.append({
                    'y': i,
                    'a': '0',
                    'b': '0',
                    'c': '0'
                })
            i = move_date_back(i, 1)

        ans.sort(key=lambda x: x['y'])
        for column in ans:
            date = column['y']
            column['y'] = map_month[date[1] - 1] + ' ' + str(date[0])
        return ans, top_three

    def get_data_for_categorization(self):
        pass

    def get_trips_this_month(self, year, month):
        trips = filter(lambda x: x.trip_date, self.all_trips)
        trips = list(filter(lambda tr: tr.trip_date.year == year and tr.trip_date.month == month, trips))
        return trips

    def get_amount_spent_on_fav_product(self, fav_product, year, month):
        trips = self.get_trips_this_month(year, month)

        res = sum(
            sum([
                purchase.price
                for purchase in trip.list_of_purchases if purchase.name_of_product.lower().count(fav_product.lower())
            ])
            for trip in trips
        )

        return round(res, 2)

    def get_average_receipt(self, year, month):
        trips = self.get_trips_this_month(year, month)

        if not trips:
            return 0

        res = sum(
            trip.receipt_amount
            for trip in trips
        ) / len(trips)

        return round(res, 2)

    def get_number_of_trips(self, year, month):
        trips = self.get_trips_this_month(year, month)
        return len(trips)






