from abc import abstractmethod, ABCMeta
from pytesseract import image_to_string
from algorithm.Meteocr import Meteocr


class OcrAdapter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def recognize(self, img):
        pass


class TesseractAdapter(OcrAdapter):
    def recognize(self, img):
        return image_to_string(img, lang='rus')


class MeteocrAdapter(OcrAdapter):
    PT_THRESHOLD = 93

    def recognize(self, img, context=Meteocr.FULL_CONTEXT):
        img_vector = Meteocr.vectorize(img)
        if img_vector.sum() > self.PT_THRESHOLD:  # todo: train on .
            return '.'
        return Meteocr().calculate(
            img_vector, context=context
        )
