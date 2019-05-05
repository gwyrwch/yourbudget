from algorithm.readers import *
from datahandling.ShoppingHistory import ShoppingHistory
from algorithm.ReceiptReader import ReceiptReader
import json
import os


class UserData:
    @staticmethod
    def get_history(username):
        sh = ShoppingHistory.objects(username=username)
        if sh.count() == 0:
            sh = ShoppingHistory(username=username)
            sh.save()
            return sh
        else:
            return sh.get()

    # def save_purchase_info(self, receipt_path):
    #     receipt_data = KoronaReceiptReader.extract_info(ReceiptReader.convert_to_receipt(receipt_path))
    #     self.list_of_purchases.append(receipt_data)
    #
    #     with open(self.data_file, "w") as write_file:
    #         json.dump(receipt_data, write_file, cls=AutoJSONEncoder, ensure_ascii=False, indent=4)
