"""
A simple one-hot encoder.
"""
import numpy as np


class SimpleOneHotEncoder:
    def __init__(self, categories: list, handle_unknown='error'):
        if handle_unknown != 'error' and handle_unknown != 'ignore':
            raise ValueError(f'Invalid value unk strategy {handle_unknown}')

        self.__cat_to_index = {cat: i for i, cat in enumerate(categories)}
        self.__handle_unknown = handle_unknown
        self.__categories = set(categories)

    def encode(self, label):
        """Returns np array"""
        in_cat = label in self.__categories
        if not in_cat and self.__handle_unknown == 'error':
            raise ValueError(f"Invalid label {label}")

        result = np.zeros((len(self.__categories), ), dtype=np.float)

        if in_cat:
            result[self.__cat_to_index[label]] = 1.0

        return result


if __name__ == '__main__':
    test_encoder = SimpleOneHotEncoder(['pi', 'min', 'max', 'stationnaire', 'hausse', 'baisse'],
                                       handle_unknown='ignore')
    print(test_encoder.encode('ma'))
