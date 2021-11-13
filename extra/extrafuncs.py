"""Дополнительные полезные функции."""

import itertools


def islice_dict(dictionary, diapason):
    """
    Принимает словарь и делит его на диапазоны.
    
    Принимает на вход словарь и длину диапазона.
    Отдает генераторы ключей словаря, равные числу диапазонов,
    не включая неполный последний диапазон, если он будет.
    Т.е. делит словарь на равные части.
    """
    for i in range (len(dictionary)//diapason):
        yield itertools.islice(
            dictionary,
            diapason * i,       # start
            diapason * (i + 1)  # stop
        )


if __name__ == '__main__':
    a = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    d = 3
    for t in islice_dict(a, d):
        print(t)
        for key in t:
            print('--->', f'{key}:', a[key])