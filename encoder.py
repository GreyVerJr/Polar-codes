from decimal import *
from math import log2
from random import randint
import numpy as np


def calc_rs(e=0.3, n=10):
    """
    Вычисляет и возвращает reliability sequence

    :param e: вероятность ошибки
    :param n: глубина дерева
    :return: reliability sequence
    """

    def polarise(p, depth=0):
        """
        Рекурсивно вычислят вероятность ошибки на каждой позиции в блоке и записывает ее в массив polarisation

        :param p: вероятность ошибки
        :param depth: глубина дерева
        :return: З
        """
        if depth == n:
            polarisation.append(Decimal(p))
            return p
        depth += 1
        return [polarise(Decimal(p ** 2), depth), polarise(Decimal(p * (2 - p)), depth)]

    getcontext().prec = 100
    polarisation = []
    rs = []
    polarise(e)
    polarisation2 = polarisation.copy()

    for i in range(len(polarisation)):
        min_index = polarisation.index(min(polarisation2))
        min_index2 = polarisation2.index(min(polarisation2))
        rs.append(min_index)
        polarisation2.pop(min_index2)
    return rs


if __name__ == "__main__":
    E = 0.3  # Вероятность ошибки
    N = 8  # Длина блока
    n = int(log2(N))
    K = 6  # Длина сообщения
    msg = [randint(0, 1) for i in range(K)]  # Случайное сообщение
    U = [0] * N
    RS = calc_rs(E, n)
    for i in range(N - K, len(RS)):
        U[RS[i]] = msg[i - N + K]

    U = np.array(U)  # Блок до поляризации
    g = np.array([[1, 0], [1, 1]])
    G = g
    for i in range(n-1):
        G = np.kron(G, g)  # Произведение кронекера

    answer = np.dot(U, G) % 2  # Блок после поляризации
    print("Massage:             ", msg)
    print("Reliability sequence:", RS)
    print("U:                   ", U)
    print("answer:              ", answer)

