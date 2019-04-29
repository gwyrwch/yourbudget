class Receipt:
    def __init__(self, lines):
        self.img_lines = lines

    @property
    def average_height(self):
        res = sum(map(lambda x: x.size[1], self.img_lines))
        return res // len(self.img_lines)
