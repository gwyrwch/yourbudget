from queue import Queue
from algorithm.Region import Region
from math import inf

DIRECTIONS = [
    [0, 1], [1, 0], [0, -1], [-1, 0]
]


class RegionFinder:
    @classmethod
    def valid(cls, matrix, x, y, pixel=1):
        """
        Checks whether the given point is in matrix and value is equal to pixel

         :param matrix
             image converted to n x m matrix
         :param x
             x-coordinate of point
         :param y
             y-coordinate of point
         :param pixel
            desired value of matrix[x][y]

         :returns
           True or False
       """
        if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[x]):
            return False
        if matrix[x][y] == pixel:
            return True
        return False

    @classmethod
    def border_cell(cls, x, y, n, m):
        """
        Checks whether the given point is on border of matrix

         :param x
             x-coordinate of point
         :param y
             y-coordinate of point
         :param n
             height of matrix
         :param m
             width of matrix

         :returns
           True or False
       """
        if x == 0 or y == 0 or x == n - 1 or y == m - 1:
            return True
        return False

    @classmethod
    def find_left_point(cls, n, m, matrix):
        """
        Finds some black pixel at the top-left part of the matrix

         :param n
             height of matrix
         :param m
             width of matrix
         :param matrix
             image converted to n x m matrix

         :returns
           (x, y) or None
       """
        for i in range(n):
            for j in range(m // 2):
                if matrix[i][j] == 1:
                    return i, j
        return None

    @classmethod
    def find_right_point(cls, n, m, matrix):
        """
        Finds some black pixel at the top-right part of the matrix

         :param n
             height of matrix
         :param m
             width of matrix
         :param matrix
             image converted to n x m matrix

         :returns
           (x, y) or None
       """
        for i in range(n):
            for j in reversed(range(m // 2, m)):
                if matrix[i][j] == 1:
                    return i, j
        return None

    @classmethod
    def find_closest(cls, n, m, matrix, sx, sy, pixel):
        """
          Breadth-first-search from a single point; finds first cell with value equal to pixel.

          :param n
              height of matrix
          :param m
              width of matrix
          :param matrix
              image converted to n x m matrix
          :param sx
              x-coordinate where to start
          :param sy
              y-coordinate where to start
          :param pixel
              finds first cell with value equal to this

          :returns
            (x, y) or None
        """
        used = set()

        q = Queue()
        q.put((sx, sy))

        while not q.empty():
            x, y = q.get()

            if cls.valid(matrix, x, y, pixel):
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
    def bfs(cls, n, m, start_x, start_y, matrix, pixel, used):
        """
            Breadth-first-search from a single point (start_x, start_y)

            :param n
                height of matrix
            :param m
                width of matrix
            :param start_x,
                x-coordinate where to start
            :param start_y
                y-coordinate where to start
            :param matrix
                image converted to n x m matrix
            :param pixel
                function searches on regions completely from pixel

            :returns
                found Region
        """
        x1, y1 = inf, inf
        x2, y2 = -x1, -y1

        q = Queue()
        q.put((start_x, start_y))

        pixels_count = 0
        while not q.empty():
            x, y = q.get()

            if type(used) is set:
                if (x, y) in used:
                    continue
                used.add((x, y))
            elif type(used) is list:
                if used[x][y]:
                    continue
                used[x][y] = True
            else:
                raise TypeError('used must be matrix or set')

            pixels_count += 1

            x1 = min(x1, x)
            y1 = min(y1, y)
            x2 = max(x2, x)
            y2 = max(y2, y)

            for d in range(4):
                dx, dy = DIRECTIONS[d]
                nx, ny = x + dx, y + dy

                if cls.valid(matrix, nx, ny, pixel):
                    q.put((nx, ny))

        return Region(
            x1, y1, x2, y2, pixels_count
        )

    @classmethod
    def find_single_region(cls, n, m, start_x, start_y, matrix, pixel):
        return cls.bfs(n, m, start_x, start_y, matrix, pixel, used=set())

    @classmethod
    def find_regions(cls, n, m, matrix, pixel=1, start_from_border=False, return_visited=False):
        """
        Breadth-first-search

        :param n
            height of matrix
        :param m
            width of matrix
        :param matrix
            image converted to n x m matrix
        :param start_from_border
            searches regions only starting from border
        :param pixel
            function searches on regions completely from pixel
        :param return_visited
            returns used matrix

        :returns
            list of detected regions
        """

        used = [
            [
                False
                for _ in range(m)
            ]
            for _ in range(n)
        ]

        regions = []

        for i in range(n):
            for j in range(m):
                if start_from_border and not cls.border_cell(i, j, n, m):
                    continue
                if not used[i][j] and matrix[i][j] == 1:
                    regions.append(
                        cls.bfs(
                            n, m, start_x=i, start_y=j, matrix=matrix, pixel=1, used=used
                        )
                    )

        if return_visited:
            return used

        return regions

    STAR = 0.5295815295815296

    @classmethod
    def filter_regions(cls, regions, approx_type, eps=0.07):
        return [
            reg
            for reg in regions
            if abs(approx_type - reg.colored_rate) < eps
        ]
