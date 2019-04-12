class KoronaReceiptParser:
    @classmethod
    def extract_info(cls, receipt):
        extracted_data = []

        for i in range(len(receipt.info)):
            if receipt.info[i].count('=') == 2:
                try:
                    name = receipt.info[i - 1]
                    raw_price = receipt.info[i].split()[-1][1:]

                    extracted_data.append(
                        (name, raw_price)
                    )
                except:
                    pass

        return extracted_data
