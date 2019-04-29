import cv2, numpy
from PIL import Image


class TextReader:
    @classmethod
    def purchases_to_text(cls, purchases, reader):
        print('start reading text')
        result = []
        for (name, price) in purchases:
            price_cv2 = numpy.array(price)

            price_cv2, _ = ContourFinder.apply_contours(price_cv2)
            price = Image.fromarray(price_cv2)

            price.show()
            result.append((reader(name, lang='rus'), reader(price)))

        return result


class ContourFinder:
    @classmethod
    def apply_contours(cls, im_cv2):
        contours, hierarchy = cv2.findContours(im_cv2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        areas = [
            cv2.contourArea(c)
            for c in contours
        ]

        sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)
        if not sorted_areas:
            return None

        large_contour = sorted_areas[0][1]

        im_cv2 = cv2.drawContours(im_cv2, [
            c[1]
            for c in sorted_areas[1:]
        ], -1, (0,255,0), 1)

        return im_cv2, large_contour
