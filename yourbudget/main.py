from algorithm.KoronaReceiptReader import KoronaReceiptParser
from algorithm.ReceiptReader import ReceiptReader
from datahandling.User import User
import os

def test_tesser():
    TESTS_PATH = 'yourbudget/algorithm/tests/'
    tests = os.listdir(TESTS_PATH)
    test_path = TESTS_PATH + tests[-1]

    r = ReceiptReader.convert_to_receipt(test_path)
    exit(0)

if __name__ == '__main__':
    test_tesser()

