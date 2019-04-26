from algorithm.readers import *
from services.AutoJSONEncoder import AutoJSONEncoder
from services.AutoJsonDecoder import AutoJSONDecoder
from algorithm.ReceiptReader import ReceiptReader
import json


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.data_file = ''.join([username, '_data', '.json'])
        self.list_of_purchases = []

    def save_purchase_info(self, receipt_path):
        receipt_data = KoronaReceiptReader.extract_info(ReceiptReader.convert_to_receipt(receipt_path))
        self.list_of_purchases.append(receipt_data)

        with open(self.data_file, "w") as write_file:
            json.dump(receipt_data, write_file, cls=AutoJSONEncoder, ensure_ascii=False, indent=4)

    def get_all_purchases(self):
        with open(self.data_file, 'r') as read_file:
            data = json.load(read_file, cls=AutoJSONDecoder)

            print(data)
