class DistFunctionFabric:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def eval(self, pt):
        x, y = pt
        return (x - self.x) ** 2 + (y - self.y) ** 2
