import os
from algorithm.ReceiptReader import ReceiptReader
from pytesseract import image_to_string as reader
from PIL import Image
from algorithm.Meteocr import MeteocrTrainer, Meteocr
from collections import defaultdict

def prepare_samples(tests_path):
    tests = os.listdir(tests_path + 'for_samples')
    from algorithm.TextReader import TextReader

    cc = 0

    for t in tests:
        if t == '.DS_Store':
            continue
        path = os.path.join(tests_path, 'for_samples', t)
        print('preparing samples for {}'.format(path))

        img = ReceiptReader.preprocess_image(path)
        lines = ReceiptReader.find_unparsed_lines(img)
        print('algorithm finished successfully')

        os.system('rm -r {}'.format(tests_path + 'samples_unknown_char'))
        os.mkdir(tests_path + 'samples_unknown_char')

        for l in lines:
            samples = TextReader.split_into_columns(l)
            for s in samples:
                s = ReceiptReader.image_in_box(s)

                m, n = s.size
                s.save(tests_path + 'samples_unknown_char/{}_{}_?_{}.png'.format(m, n, cc))
                cc += 1
    print('finished creating samples')

class Statistics:
    def __init__(self, values=None):
        if values is None:
            values = list()
        self.values = values

    def append(self, x):
        self.values.append(x)

    def avg(self):
        return sum(self.values) / len(self.values)

    def median(self):
        return self.quantile(1, 2)

    def quantile(self, p, q):
        return sorted(self.values)[len(self.values) * p // q]

    def good_range(self):
        return range(self.median(), self.quantile(9, 10) + 1)

    def display(self):
        print(
            '\n'.join(
                [
                    'min = {}'.format(min(self.values)),
                    'max = {}'.format(max(self.values)),
                    'avg = {}'.format(self.avg()),
                    'kva5/10 = {}'.format(self.median()),
                    'kva7/10 = {}'.format(self.quantile(7, 10)),
                    'kva9/10 = {}'.format(self.quantile(9, 10))
                ]
            )
        )



def process_samples(tests_path):
    samples_path = os.path.join(tests_path, 'samples_unknown_char')

    width_stat, height_stat = Statistics(), Statistics()
    for sample in os.listdir(samples_path):
        m, n, c, id = sample.split('_')
        m, n = map(int, [m, n])
        width_stat.append(m)
        height_stat.append(n)

    # width_stat.display()
    # print()
    # height_stat.display()

    cnt = 0

    for sample in os.listdir(samples_path):
        _m, _n, c, id = sample.split('_')

        s = Image.open(os.path.join(samples_path, sample))
        m, n = s.size

        s = s.resize((m * 10, n * 10), Image.BOX)
        if m in width_stat.good_range() and n in height_stat.good_range():
            # t = reader(s, lang='rus')

            cnt += 1
    print(cnt)


def main_training():
    # MeteocrTrainer.run_training(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '*', '='])
    MeteocrTrainer.run_training(
        [
            'а', 'А', 'б', 'Б', 'в', 'г', 'д', 'е', 'Е',     'ж', 'и', 'нн',
            'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
            'ч', 'ш', 'ю', 'я', '$', '='
         ]
    )
    Meteocr().save_theta()


def test_meteocr(TESTS_PATH, verbose=False):
    tests_path = os.path.join(TESTS_PATH, 'tests_for_meteocr')
    ok, wa = 0, 0

    # context = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '*', '=']
    context = [
        'а', 'А', 'б', 'Б', 'в', 'г', 'д', 'е', 'Е', 'ж', 'и', 'нн', 'к', 'л',
        'м', 'н', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'ю', 'я', '$', '='
    ]

    cnt_ok = defaultdict(int)
    cnt_wa = defaultdict(int)

    for d in os.listdir(tests_path):
        if d == '.DS_Store':
            continue
        img = Image.open(os.path.join(tests_path, d))
        ans = d.split('_')[0]

        img_vector = Meteocr().vectorize(img)

        if ans not in context:
            continue

        res = Meteocr().calculate(img_vector, context, verbose)

        if res == ans:
            ok += 1
            print('OK {}'.format(res))

            cnt_ok[ans] += 1
        else:
            wa += 1
            print('WA {} expected {}'.format(res, ans))
            cnt_wa[ans] += 1
            if verbose:
                img.show()

    print('Total {}% ok'.format(ok / (ok + wa) * 100))
    for c in context:
        ok = cnt_ok[c]
        total = cnt_ok[c] + cnt_wa[c]

        if total == 0:
            print('No samples for {}'.format(c))
        else:
            print('{} ok for {}'.format(ok / total * 100, c))




# more data!
# add . to characters