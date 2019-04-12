from PIL import Image
import pytesseract
from yourbudget.Receipt import Receipt


class ReceiptReader:
    @classmethod
    def preetify_token(cls, t):
        # todo: научится пользоваться
        if t == u'КИДКА':
            return 'СКИДКА'

        return t

    @classmethod
    def preetify_line(cls, s):
        tokens = s.split()

        tokens = [
            cls.preetify_token(t)
            for t in tokens
        ]

        return ' '.join(
            tokens
        )

    @classmethod
    def convert_to_receipt(cls, image_path):
        img = Image.open('test2.jpeg')
        text = pytesseract.image_to_string(Image.open('test2.jpeg'), lang='rus')

        lines = text.splitlines()

        lines = [
            cls.preetify_line(s)
            for s in lines
        ]

        lines = [s for s in lines if len(s) > 0]
        return Receipt(lines)
