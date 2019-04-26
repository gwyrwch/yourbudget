from algorithm.readers import *


class ShopDeducter:
    available_readers = [
        (u'ООО Либретик', SosediReceiptReader),
        (u'ООО "ТАБАК ИНВЕСТ"', KoronaReceiptReader),
        # todo biggz
    ]

    @classmethod
    def string_distance(cls, s1, s2):
        if s1.count(s2):
            return 1.0

        n, m = len(s1), len(s2)

        dp = [
            [0] * (m + 1)
            for _ in range(n + 1)
        ]

        res = 0
        for i in range(n + 1):
            for j in range(m + 1):
                if i == n and j == m:
                    res = dp[i][j]
                elif i == n or j == m:
                    dp[n][m] = max(dp[n][m], dp[i][j])
                else:
                    dp[i + 1][j] = max(dp[i + 1][j], dp[i][j])
                    dp[i][j + 1] = max(dp[i][j + 1], dp[i][j])
                    if s1[i] == s2[j]:
                        dp[i + 1][j + 1] = max(dp[i + 1][j + 1], dp[i][j] + 1)
        return res / len(s1)


    @classmethod
    def deduct_shop(cls, raw_shop_name):
        best_result = 0.5
        best_reader = DefaultReceiptReader
        for name, reader in cls.available_readers:
            distance = cls.string_distance(name, raw_shop_name)
            if distance > best_result:
                best_result = distance
                best_reader = reader
        return best_reader
