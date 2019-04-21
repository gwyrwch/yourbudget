from algorithm.KoronaReceiptReader import KoronaReceiptParser
from algorithm.ReceiptReader import ReceiptReader
from datahandling.User import User

def test_tesser():
    r = ReceiptReader.convert_to_receipt('yourbudget/algorithm/test2_cut2.png')

    exit(0)

if __name__ == '__main__':
    # test_tesser()

    usr = User('temp_user', 'temp_user@gmail.com')
    usr.save_purchase_info('yourbudget/algorithm/test2.jpeg')
    # usr.save_purchase_info('yourbudget/algorithm/test3.JPG')

    usr.get_all_purchases()


