from PIL import Image, ImageDraw

from algorithm.readers import *
from algorithm.Region import Region
from algorithm.Receipt import Receipt
from algorithm.RegionFinder import RegionFinder
from algorithm.DistFunctionFabric import DistFunctionFabric
from math import atan, pi

import cv2
import pyocr
import pyocr.builders
from pytesseract import image_to_string as img_to_str
import numpy

DEBUG = False

USE_PYOCR = False
USE_UPDATE = False

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
        img = cls.rotate_image(img)

        matrix = cls.get_matrix_from_image(img)
        m, n = img.size
        matrix.append([0] * m)
        n += 1

        img_lines = []
        in_region = True
        last_line = 0

        for i in range(n):
            white_line = True

            fp, lp = None, None

            for j in range(m):
                if matrix[i][j] == 0:
                    fp = j
                    break

            for j in range(m):
                if matrix[i][j] == 0:
                    lp = j

            if fp is None:
                white_line = False

            if white_line:
                for j in range(fp, lp + 1):
                    if matrix[i][j] == 1:
                        white_line = False

            if lp - fp < m // 2:
                white_line = False

            if not white_line:
                in_region = False

            if white_line and not in_region:
                img_lines.append(Image.fromarray(
                    numpy.asarray(
                        [
                            [
                                255 if matrix[k][j] == 0 else 0
                                for j in range(m)
                            ]
                            for k in range(last_line, i + 1)
                        ], numpy.uint8
                    )
                ))

                in_region = True
                last_line = i

        if len(img_lines) == 1:
            return img_lines

        result = []
        for img in img_lines:
            result += cls.find_unparsed_lines(img)
        return result

    @classmethod
    def rotate_image(cls, img):
        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        left_point = RegionFinder.find_left_point(n, m, matrix)
        right_point = RegionFinder.find_right_point(n, m, matrix)

        if left_point is None or right_point is None:
            return img

        if DEBUG:
            draw = ImageDraw.Draw(img)

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

        return rot_img

    @classmethod
    def compress_image(cls, img):
        BUBEN = 1440

        m, n = img.size
        if n < BUBEN:
            return img

        newn = BUBEN
        newm = int(1. * BUBEN / n * m)

        img = img.resize((newm, newn), Image.BOX)
        return img

    availiable_readers = [
        (u'ООО Либретик', SosediReceiptReader),
        (u'ООО "ТАБАК ИНВЕСТ"', KoronaReceiptReader),
        # todo biggz
    ]

    @classmethod
    def string_distance(cls, s1, s2):
        if s1.count(s2):
            return 1.0

        n, m = len(s1), len(s2)

        dp = [
            [0] * (m + 1)
            for _ in range(n + 1)
        ]

        res = 0
        for i in range(n + 1):
            for j in range(m + 1):
                if i == n and j == m:
                    res = dp[i][j]
                elif i == n or j == m:
                    dp[n][m] = max(dp[n][m], dp[i][j])
                else:
                    dp[i + 1][j] = max(dp[i + 1][j], dp[i][j])
                    dp[i][j + 1] = max(dp[i][j + 1], dp[i][j])
                    if s1[i] == s2[j]:
                        dp[i + 1][j + 1] = max(dp[i + 1][j + 1], dp[i][j] + 1)
        print(res, len(s1))
        return res / len(s1)

    @classmethod
    def deduct_shop(cls, raw_shop_name):
        best_result = 0.5
        best_reader = DefaultReceiptReader
        for name, reader in cls.availiable_readers:
            distance = cls.string_distance(name, raw_shop_name)
            if distance > best_result:
                best_result = distance
                best_reader = reader
        return best_reader

    @classmethod
    def convert_to_receipt(cls, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)

        # todo: обрезать
        # todo: избавится от шума по краям

        receipt_img = Image.open(filename)
        receipt_img = cls.compress_image(receipt_img)

        lines = cls.find_unparsed_lines(receipt_img)

        if USE_PYOCR:
            raise NotImplementedError('pyocr is not implemented')
            # tools = pyocr.get_available_tools()
            #
            # tool = tools[0]
            #
            # img = Image.open(image_path)
            # img = img.convert("L")
            # img = cut_noise(img)
            #
            # text = tool.image_to_string(img, lang='rus')
        else:
            raw_shop_name = ' '.join([
                img_to_str(l, lang='rus')
                for l in lines[0:3]
            ])

        reader = cls.deduct_shop(raw_shop_name)
        print(reader)
        return reader.extract_info(Receipt(lines))
