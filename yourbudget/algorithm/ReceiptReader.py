from PIL import Image, ImageDraw

from algorithm.Region import Region
from algorithm.Receipt import Receipt
from algorithm.RegionFinder import RegionFinder
from algorithm.DistFunctionFabric import DistFunctionFabric
from math import atan, pi

import cv2
import pyocr
import pyocr.builders
import pytesseract
import numpy

DEBUG = False

USE_PYOCR = False
USE_UPDATE = True

def cut_noise(image):
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')

class ReceiptReader:
    @classmethod
    def preetify_token(cls, t):
        # todo: находить похожие слова в словаре
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

    @staticmethod
    def get_matrix_from_image(img):
        matrix = numpy.asarray(img)
        m, n = img.size

        matrix = [
            [
                1 if matrix[i,j] < 128 else 0
                for j in range(m)
            ]
            for i in range(n)
        ]

        return matrix

    # todo: refactor
    @classmethod
    def find_unparsed_lines(cls, img):
        draw = ImageDraw.Draw(img)

        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        lines = []
        in_region = False

        for i in range(n):
            ok = True

            fp, lp = None, None

            for j in range(m):
                if matrix[i][j] == 0:
                    fp = j
                    break

            for j in range(m):
                if matrix[i][j] == 0:
                    lp = j

            if fp is None:
                ok = False

            if ok:
                for j in range(fp, lp + 1):
                    if matrix[i][j]:
                        ok = False

            if lp - fp < m // 2:
                ok = False

            if not ok:
                in_region = False

            if ok and not in_region:
                lines.append(i)
                # if DEBUG:
                draw.line((0, i, m - 1, i), fill=128)
                in_region = True

        # if DEBUG:
        img.show()

        return lines

    @classmethod
    def rotate_image(cls, filename):
        img = Image.open(filename)
        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        all_regions = RegionFinder.find_regions(n, m, matrix)
        stars = RegionFinder.filter_regions(all_regions, RegionFinder.STAR)

        pts = [
            star.get_center()
            for star in stars
        ]

        left_point = min(pts, key=DistFunctionFabric(0, 0).eval)
        right_point = min(pts, key=DistFunctionFabric(0, m - 1).eval)

        if DEBUG:
            draw = ImageDraw.Draw(img)

            for star in stars:
                draw.rectangle(star.bounding_box, fill="red")

            print('Left point = ', left_point)
            print('Right point = ', right_point)

            draw.rectangle(Region.make_box_around(left_point), fill="blue")
            draw.rectangle(Region.make_box_around(right_point), fill="blue")

            img.show()

        dx = -left_point[0] + right_point[0]
        dy = abs(left_point[1] - right_point[1])

        angle = atan(dx / dy) / pi * 180

        rot_img = img.rotate(angle, fillcolor=255)

        if DEBUG:
            rot_img.show()

        rot_img.save(filename)

    @classmethod
    def convert_to_receipt(cls, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)

        cls.rotate_image(filename)
        cls.find_unparsed_lines(Image.open(filename))

        # if USE_PYOCR:
        #     tools = pyocr.get_available_tools()
        #
        #     tool = tools[0]
        #
        #     img = Image.open(image_path)
        #     img = img.convert("L")
        #     img = cut_noise(img)
        #
        #     text = tool.image_to_string(img, lang='rus')
        # elif USE_UPDATE:
        #     text = pytesseract.image_to_string(Image.open(filename), lang='rus')
        # else:
        #     text = pytesseract.image_to_string(Image.open(image_path), lang='rus')

        # lines = text.splitlines()
        #
        # lines = [
        #     cls.preetify_line(s)
        #     for s in lines
        # ]
        #
        # lines = [s for s in lines if len(s) > 0]
        #
        # for l in lines:
        #     print(l)

        # return Receipt(lines)
