import cv2, numpy
from PIL import Image
import logging

from datahandling.ShoppingTrip import Purchase


class TextReader:
    COUNTOURS = False

    @classmethod
    def purchases_to_text(cls, purchases, reader, shop_template_reader):
        logging.info('start reading text')
        result = []
        for (name, price) in purchases:
            if cls.COUNTOURS:
                price_cv2 = numpy.array(price)

                price_cv2, _ = ContourFinder.apply_contours(price_cv2)
                price = Image.fromarray(price_cv2)

            price_splitted = cls.split_into_columns(price)
            price_splitted = reversed(price_splitted)

            price = ''.join(
                cls.digit_read(reader, single_digit_png)
                for single_digit_png in price_splitted
            )

            logging.info(price)
            price = shop_template_reader.convert_to_float(price)
            result.append(Purchase(name_of_product=reader(name, lang='rus'), price=price))

        return result

    # Fixme: should be captured from the current size of image
    INTEPS = 4

    @classmethod
    def digit_read(cls, reader, single_digit_png):
        from algorithm.ReceiptReader import ReceiptReader
        matrix = ReceiptReader.get_matrix_from_image(single_digit_png)
        matrix = ReceiptReader.make_box(matrix)

        # ReceiptReader.get_image_from_matrix(matrix).show()

        best_similarity = 0
        result = '-'

        if len(matrix) < cls.INTEPS or len(matrix[0]) < cls.INTEPS:
            return '.'

        for c, mat_char in cls.PRICE_CHARS:
            mat = [
                [
                    0 if j == '0' else 1
                    for j in i
                ]
                for i in mat_char.splitlines()[1:-1]
            ]
            mat = cls.resize_mat(mat, len(matrix), len(matrix[0]))

            cur_similarity = cls.similarity(mat, matrix)

            if cur_similarity > best_similarity:
                best_similarity = cur_similarity
                result = c
        logging.info('find char {} with similarity {}'.format(result, best_similarity))
        return result

    PRICE_CHARS = (
        (
            '1',
            '''
001100
011100
111100
000100
000100
000100
000100
000100
000100
000100
000100
000100
000100
000110
001111
            '''
         ),
        (
            '3',
            '''
00111100
01100110
11000011
00000011
00000001
00000001
00000111
00011110
00000111
00000001
00000001
00000001
11000011
01100110
00111100
            '''
        ),
        (
            '#',
            '''
1111111
1111111
0000000
0000000
0000000
1111111
1111111
0000000
0000000
1111111
1111111
            '''
        ),
        (
            '9',
            '''
0011110
1110011
1100001
1000001
1000001
1000001
1000001
1100001
1110011
0011101
0000001
1000001
1100001
0110011
0011110
            '''
        ),
        (
            '=',
            '''
11111111
11111111
00000000
00000000
00000000
00000000
11111111
11111111
            '''
        ),
        (
            '5',
            '''
01111110
11100000
11000000
10000000
10000000
11111000
11111100
11000110
10000011
00000001
00000001
00000001
10000001
11000011
01111110
00111100
            '''
        ),
        (
            '*',
            '''
00011000
10011011
11111110
01111110
00111100
00111100
00111100
01111110
11001011
00011000
            '''
        ),
        (
            '7',
            '''
1111111
0000011
0000011
0000011
0000110
0000100
0001100
0001100
0001100
0011100
0011000
0011000
0011000
0011000
0011000
0010000
            '''
        ),
        (
            '2',
            '''
01111100
11000011
10000001
10000001
00000001
00000001
00000011
00000010
00000110
00001100
00011000
00110000
01100000
11111111
11111111
            '''
        ),
        (
            '0',
            '''
0011100
0100010
1000001
1000001
1000001
1000001
1000001
1000001
1000001
1000001
1000001
1000001
1100011
0111110
            '''
        ),
        (
            '8',
            '''
000111000
011101100
010000110
110000010
110000010
011000110
001111100
001111100
011100110
011000010
110000010
110000011
110000011
111000111
011111110
001111100
            '''
        ),
        (
            '4',
            '''
000000100
000001100
000011100
000011100
000110100
000100100
000100100
001000100
001000100
010000100
111001110
111111111
000001100
000000100
000000100
000000100
            '''
        ),
        (
            '6',
            '''
001111000
011101110
110000011
110000000
110000000
110000000
011111100
011100110
011000010
010000011
010000001
010000001
100000010
110000110
111001110
011111100
            '''
        ),
        (
            '#',
            '''
0000011
0001111
1111100
0110000
0000000
0000011
0001100
1110000
0000000
0000011
0001100
1110000
            '''
        )
    )

    @classmethod
    def similarity(cls, mat1, mat2):
        n = len(mat1)
        m = len(mat1[0])

        result = 0

        for i in range(n):
            for j in range(m):
                if mat1[i][j] == mat2[i][j]:
                    result += 1
        return result

    @classmethod
    def resize_mat(cls, matrix, n, m):
        from algorithm.ReceiptReader import ReceiptReader
        img = ReceiptReader.get_image_from_matrix(matrix)
        img = img.resize((m, n), Image.BOX)
        return ReceiptReader.get_matrix_from_image(img)

    @classmethod
    def split_into_columns(cls, img):
        from algorithm.ReceiptReader import ReceiptReader
        img = img.rotate(90, expand=1, fillcolor=255)

        lines = ReceiptReader.find_unparsed_lines(img, no_rotate=True)

        lines = [
            l.rotate(-90, expand=1, fillcolor=255)
            for l in lines
        ]

        return lines


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
        ], -1, (0, 255, 0), 1)

        return im_cv2, large_contour
