from PIL import Image
import pytesseract

if __name__ == '__main__':
    import ReceiptReader, KoronaReceiptReader
    receipt = ReceiptReader.ReceiptReader.convert_to_receipt('test1.jpeg')
    KoronaReceiptReader.KoronaReceiptParser.extract_info(receipt)

    pass