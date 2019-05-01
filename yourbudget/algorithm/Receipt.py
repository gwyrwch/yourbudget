class Receipt:
    def __init__(self, lines):
        self.img_lines = lines

    @property
    def average_height(self):
        res = sorted(map(lambda x: x.size[1], self.img_lines))
        return res[len(res) // 2]
