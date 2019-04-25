class Region:
    def __init__(self, x1, y1, x2, y2, black_pixels, all_pixels=None):
        self.bounding_box = ((y1, x1), (y2, x2))
        self.black_pixels = black_pixels
        self.all_pixels = all_pixels

    @property
    def area(self):
        (y1, x1), (y2, x2) = self.bounding_box
        return (x2 - x1 + 1) * (y2 - y1 + 1)

    @property
    def colored_rate(self):
        return 1. * self.black_pixels / self.area

    def get_center(self):
        (y1, x1), (y2, x2) = self.bounding_box
        return (x1 + x2) / 2, (y1 + y2) / 2

    @staticmethod
    def make_box_around(pt):
        x, y = pt
        return (
            (y - 5, x - 5), (y + 5, x + 5)
        )
