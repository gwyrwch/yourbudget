import csv
from math import exp
import numpy as np
import os
from PIL import Image
from random import randrange


class ValueFiles:
    theta_trained = 'yourbudget/algorithm/theta_trained.csv'
    theta_trained_backup = 'yourbudget/algorithm/theta_trained_backup.csv'
    samples_png_dir = 'yourbudget/algorithm/tests/samples_known_char'


def f(z):
    if z > 100:
        return 1
    if z < -100:
        return 0
    return 1 / (1 + exp(-z))


EPS = 10 ** -10


class Meteocr:
    THETA = {}

    RUSSIAN_LETTERS = [
        'а', 'А', 'б', 'Б', 'в', 'г', 'д', 'е', 'Е', 'ж', 'и', 'нн', 'к', 'л',
        'м', 'н', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'ю', 'я'
    ]
    DIGITS = list(map(str, range(0, 10)))
    SPEC_CHARACTERS = ['$', '*', '=', '@']

    DIGIT_CONTEXT = DIGITS + SPEC_CHARACTERS
    FULL_CONTEXT = DIGITS + RUSSIAN_LETTERS + SPEC_CHARACTERS

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            if not os.path.exists(ValueFiles.theta_trained):
                raise FileNotFoundError('No such files')
            cls.instance = super(Meteocr, cls).__new__(cls)

            with open(ValueFiles.theta_trained, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    character = row[0]
                    cls.THETA[character] = np.array(list(map(float, row[1:])))

        return cls.instance

    def calculate(self, x, context, verbose=False):
        """
        :param x: array of features
        :param context:
        :param verbose:
        :return:
        """

        best_probability = -np.inf
        result = '-'

        x = np.array(x)

        for c in context:
            if c not in self.THETA:
                self.THETA[c] = np.zeros(145)

            z = (self.THETA[c] * x).sum()
            if verbose:
                print(c, ' ', round(z, 3))
            if z > best_probability:
                best_probability = z
                result = c

        if verbose:
            print(best_probability, result)
        return result

    def save_theta(self):
        os.system('cp {} {}'.format(ValueFiles.theta_trained, ValueFiles.theta_trained_backup))  # todo: sorry guys unix only
        with open(ValueFiles.theta_trained, 'w') as file:
            for character, theta_vector in self.THETA.items():
                file.write(','.join([character] + list(map(str, theta_vector.tolist()))))
                file.write('\n')

    @staticmethod
    def vectorize(img):
        from .ReceiptReader import ReceiptReader
        img = img.resize((9, 16), Image.HAMMING)
        matrix = ReceiptReader.get_matrix_from_image(img)
        return np.array(sum(matrix, [1]))


class MeteocrTrainer:
    @classmethod
    def _train(cls, character, current_theta, sample):
        """
        :param character:
        :param current_theta: np.array of 145 elements
        :param sample: array of pairs: np.array of 145 elements and character
        :return:
        """
        for iters in range(5):
            alpha = 1
            _lambda = 1

            for iterations in range(20):
                new_theta = current_theta.copy()

                for x, c in sample:
                    y = 1 if c == character else 0
                    new_theta = new_theta - alpha * (-y + f((current_theta * x).sum())) * x
                new_theta = new_theta - current_theta * alpha * _lambda

                alpha /= 2
                current_theta = new_theta
        return current_theta

    @classmethod
    def run_training(cls, characters_to_train):
        sample = []
        for d in os.listdir(ValueFiles.samples_png_dir):
            if d == '.DS_Store':
                continue
            img_vector = Meteocr.vectorize(Image.open(os.path.join(ValueFiles.samples_png_dir, d)))

            character, _ = d.split('_', 1)

            if character not in characters_to_train:
                continue

            print('Sample with character {}'.format(character))

            sample.append((img_vector, character))

        print('Now we have {} samples'.format(len(sample)))

        for c in characters_to_train:
            current_theta = Meteocr().THETA.get(c, np.zeros(145))
            old_theta = current_theta[0]
            result_theta = cls._train(
                c, current_theta, sample
            )
            if abs(old_theta - result_theta[0]) < 10**-4:
                print('Theta of {} wasn"t updated much'.format(c))
            else:
                print('Updating theta of {} to {}'.format(c, result_theta[0]))
            Meteocr.THETA[c] = result_theta
