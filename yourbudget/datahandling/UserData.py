from algorithm.readers import *
from datahandling.ShoppingHistory import ShoppingHistory
from services.AutoJSONEncoder import AutoJSONEncoder
from services.AutoJsonDecoder import decoder_fabric
from algorithm.ReceiptReader import ReceiptReader
import json
import os


class UserData:
    @staticmethod
    def get_history(username):
        data_file = ''.join([username, '_data', '.json'])
        try:
            with open(data_file, 'r') as read_file:
                data = json.load(read_file, cls=decoder_fabric(ShoppingTrip))
                assert type(data) == list
                return ShoppingHistory(data)
        except:
            print(os.system('pwd'))

            print('kek', data_file)
            return ShoppingHistory([])

    # def save_purchase_info(self, receipt_path):
    #     receipt_data = KoronaReceiptReader.extract_info(ReceiptReader.convert_to_receipt(receipt_path))
    #     self.list_of_purchases.append(receipt_data)
    #
    #     with open(self.data_file, "w") as write_file:
    #         json.dump(receipt_data, write_file, cls=AutoJSONEncoder, ensure_ascii=False, indent=4)
