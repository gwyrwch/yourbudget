from queue import Queue
from algorithm.Region import Region

DIRECTIONS = [
    [0, 1], [1, 0], [0, -1], [-1, 0]
]


class RegionFinder:
    @classmethod
    def valid(cls, matrix, x, y):
        if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[x]):
            return False
        if matrix[x][y] == 1:
            return True
        return False

    @classmethod
    def find_left_point(cls, n, m, matrix):
        for i in range(n):
            for j in range(m // 2):
                if matrix[i][j] == 1:
                    return i, j
        return None

    @classmethod
    def find_right_point(cls, n, m, matrix):
        for i in range(n):
            for j in reversed(range(m // 2, m)):
                if matrix[i][j] == 1:
                    return i, j
        return None

    @classmethod
    def find_clothest(cls, n, m, matrix, sx, sy):
        used = set()

        q = Queue()
        q.put((sx, sy))

        while not q.empty():
            x, y = q.get()

            if cls.valid(matrix, x, y):
                return x, y
            if (x, y) in used:
                continue
            if x < 0 or y < 0 or x >= n or y >= m:
                continue

            used.add((x, y))

            for d in range(4):
                dx, dy = DIRECTIONS[d]
                nx, ny = x + dx, y + dy

                q.put((nx, ny))
        return None

    @classmethod
    def find_regions(cls, n, m, matrix):
        """
        Breadth-first-search
        """

        used = [
            [
                False
                for j in range(m)
            ]
            for i in range(n)
        ]

        regions = []

        for i in range(n):
            for j in range(m):
                if not used[i][j] and matrix[i][j] == 1:
                    x1, y1 = 10 ** 100, 10 ** 100
                    x2, y2 = -x1, -y1

                    q = Queue()
                    q.put((i, j))

                    black_pixels_count = 0
                    while not q.empty():
                        x, y = q.get()

                        if used[x][y]:
                            continue

                        black_pixels_count += 1
                        used[x][y] = True

                        x1 = min(x1, x)
                        y1 = min(y1, y)
                        x2 = max(x2, x)
                        y2 = max(y2, y)

                        for d in range(4):
                            dx, dy = DIRECTIONS[d]
                            nx, ny = x + dx, y + dy

                            if cls.valid(matrix, nx, ny):
                                q.put((nx, ny))

                    regions.append(
                        Region(
                            x1, y1, x2, y2, black_pixels_count
                        )
                    )

        return regions

    STAR = 0.5295815295815296

    @classmethod
    def filter_regions(cls, regions, approx_type, eps=0.07):
        return [
            reg
            for reg in regions
            if abs(approx_type - reg.colored_rate) < eps
        ]
