import pytest
import os
from PIL import Image
from algorithm.Meteocr import *
from algorithm.character_recognition_adapters import MeteocrAdapter, TesseractAdapter


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

    @staticmethod
    @pytest.mark.parametrize(
        "img_path",
        ['yourbudget/tests/static/a.png', 'yourbudget/tests/static/0.png']
    )
    def test_adapters(img_path):
        for adapter in [MeteocrAdapter(), TesseractAdapter()]:
            c = adapter.recognize(Image.open(img_path))
            assert type(c) == str

