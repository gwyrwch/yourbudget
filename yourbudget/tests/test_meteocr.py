import pytest
import os
from PIL import Image
from algorithm.Meteocr import *


class TestMetetocr:
    @staticmethod
    @pytest.mark.parametrize(
        "img_path",
        ['yourbudget/tests/static/a.png', 'yourbudget/tests/static/0.png']
    )
    def test_vectorize(img_path):
        if not os.path.exists(img_path):
            assert False
        img = Image.open(img_path)
        vec = Meteocr.vectorize(img)
        assert vec.size == 145


