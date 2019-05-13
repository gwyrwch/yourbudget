from PIL import Image, ImageDraw

from algorithm.Region import Region
from algorithm.Receipt import Receipt
from algorithm.ShopDeducter import ShopDeducter
from algorithm.RegionFinder import RegionFinder
from algorithm.DistFunctionFabric import DistFunctionFabric
from math import atan, pi

import cv2
import pyocr
import pyocr.builders
from pytesseract import image_to_string as img_to_str
import numpy
import logging

DEBUG = False

USE_PYOCR = False
USE_UPDATE = False


class ReceiptReader:
    @staticmethod
    def get_matrix_from_image(img):
        """
        Converts image to 0/1 matrix

        :param img
            PIL gray image

        :returns
            image converted to n x m matrix
        """

        # todo: use numpy everywhere
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

    @staticmethod
    def get_image_from_matrix(matrix):
        """
        Converts 0/1 matrix to image

        :param matrix
            image converted to n x m matrix
        :returns
            PIL gray image
        """
        return Image.fromarray(
            numpy.asarray(
                [
                    [
                        (1 - matrix[i][j]) * 255
                        for j in range(len(matrix[i]))
                    ]
                    for i in range(len(matrix))
                ], numpy.uint8
            )
        )

    @classmethod
    def find_unparsed_lines(cls, img, **kwargs):
        """
        Splits an image with text into lines; rotates if necessary

        :param img
            PIL gray image
        :param no_rotate
            set this to True, if the image should not be rotated

        :returns
            list of PIL gray images -- lines of text
        """
        if not kwargs.get('no_rotate'):
            img = cls.rotate_image(img, **kwargs)

        matrix = cls.get_matrix_from_image(img)
        m = img.size[0]
        matrix.append([0] * m)
        n = len(matrix)

        img_lines = []
        in_region = True
        last_line = 0

        for i in range(n):
            white_line = True

            for j in range(m):
                if matrix[i][j] == 1:
                    white_line = False

            if not white_line:
                in_region = False

            if white_line and not in_region:
                img_lines.append(
                    cls.get_image_from_matrix(matrix[last_line:i+1])
                )

                in_region = True
                last_line = i

        if len(img_lines) == 1:
            return img_lines

        result = []
        for img in img_lines:
            result += cls.find_unparsed_lines(img, **kwargs)
        return result

    @classmethod
    def rotate_image(cls, img, **kwargs):
        """
        Rotates image with text using two points at the top; doesn't work with noisy images

        :param img
            PIL gray image
        :param debug
            set this to True, if you want to paint this point on the s

        :returns
            rotated img
        """
        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        left_point = RegionFinder.find_left_point(n, m, matrix)
        right_point = RegionFinder.find_right_point(n, m, matrix)

        if left_point is None or right_point is None:
            return img

        if DEBUG or kwargs.get('debug'):
            draw = ImageDraw.Draw(img)

            print('Left point = ', left_point)
            print('Right point = ', right_point)

            draw.rectangle(Region.make_box_around(left_point), fill="blue")
            draw.rectangle(Region.make_box_around(right_point), fill="blue")

            img.show()

        dx = -left_point[0] + right_point[0]
        dy = abs(left_point[1] - right_point[1])

        angle = atan(dx / dy) / pi * 180

        rot_img = img.rotate(angle, expand=1, fillcolor=255)

        if DEBUG:
            rot_img.show()

        return rot_img

    @classmethod
    def compress_image(cls, img):
        """
        Compresses too large image for speedup; makes image height equal to DESIRED_HEIGHT and saves proportion.

        :param img
            PIL gray image

        :returns
            compressed image
        """
        DESIRED_HEIGHT = 1440

        m, n = img.size
        if n < DESIRED_HEIGHT:
            return img

        height = DESIRED_HEIGHT
        width = int(1. * DESIRED_HEIGHT / n * m)

        img = img.resize((width, height), Image.BOX)
        return img

    @classmethod
    def make_box(cls, matrix):
        m = len(matrix[0])
        n = len(matrix)

        from math import inf
        fx, sx = inf, -inf
        fy, sy = inf, -inf

        for i in range(n):
            for j in range(m):
                if matrix[i][j]:
                    fx = min(fx, i)
                    sx = max(sx, i)
                    fy = min(fy, j)
                    sy = max(sy, j)

        if fx > sx or fy > sy:
            return []

        matrix = matrix[fx:sx + 1]
        for i in range(len(matrix)):
            matrix[i] = matrix[i][fy:sy+1]
        return matrix


    @classmethod
    def remove_border_noise(cls, img):
        """
        Removes noise from the border of the image. Works with shadows, smooth backgrounds

        :param img
            PIL gray image

        :returns
            image without noise
        """
        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        used_in_bfs = RegionFinder.find_regions(
            n, m, matrix,
            start_from_border=True,
            return_visited=True
        )

        for i in range(n):
            for j in range(m):
                if used_in_bfs[i][j]:
                    matrix[i][j] = 0

        matrix = cls.make_box(matrix)
        return cls.get_image_from_matrix(matrix)

    @classmethod
    def cut_receipt_from_raw_image(cls, img):
        """
        Searches for region with receipt on the given image and crops the whole image to this region.

        :param img
            PIL gray image

        :returns
            cropped image
        """
        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        center_x = n // 2
        center_y = m // 2

        center_x, center_y = RegionFinder.find_closest(n, m, matrix, center_x, center_y, pixel=0)

        receipt_region = RegionFinder.find_single_region(n, m, start_x=center_x,  start_y=center_y, matrix=matrix, pixel=0)

        img = img.crop(receipt_region.flat_bounding_box)
        return img

    @classmethod
    def rate_center_area(cls, img):
        # fixme: replace this code

        matrix = cls.get_matrix_from_image(img)
        m, n = img.size

        p, q = 0, 0

        fp, ls = -1, -1
        for i in range(n):
            if any(matrix[i]):
                ls = i
                if fp == -1:
                    fp = i

        center_x = (fp + ls) // 2
        if center_x == -1:
            return 0

        for i in range(n):
            for j in range(m):
                if matrix[i][j]:
                    if abs(i - center_x) < 2:
                        p += 1
                    q += 1
        if p == 0:
            img.show()
        return p / q

    @classmethod
    def convert_to_receipt(cls, image_path):
        """
        Takes a raw image and processes the full algorithm of extracting receipt data from it.

        :param image_path
            path to the photo of receipt
        :returns
            ShoppingTrip extracted from image
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        ret, gray = cv2.threshold(gray, 127, 255, 0)

        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)

        receipt_img = Image.open(filename)
        receipt_img = cls.compress_image(receipt_img)
        receipt_img = cls.cut_receipt_from_raw_image(receipt_img)
        receipt_img = cls.remove_border_noise(receipt_img)

        image_lines = cls.find_unparsed_lines(receipt_img)
        logging.info('i found {} lines'.format(len(image_lines)))
        for i in range(len(image_lines)):
            image_lines[i].save('result_lines/line{}.png'.format(i))

        if USE_PYOCR:
            raise NotImplementedError('pyocr is not implemented')
        else:
            raw_shop_name = ' '.join([
                img_to_str(l, lang='rus')
                for l in image_lines[0:3]
            ])

        reader = ShopDeducter.deduct_shop(raw_shop_name)

        logging.info('Shop deducter found ' + str(reader))
        return reader.extract_info(Receipt(image_lines), img_to_str)
