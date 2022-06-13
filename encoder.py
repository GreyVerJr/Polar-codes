from decimal import *
from random import randint

import numpy as np
from mpmath import sign

from parameters import *


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
        :return:
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


def encoder():
    msg = [randint(0, 1) for i in range(K)]  # Случайное сообщение
    U = [0] * N
    RS = []
    for i in reliability_sequence:
        if i < N:
            RS.append(i)
    for i in range(N - K, N):
        U[RS[i]] = msg[i - N + K]

    U = np.array(U)  # Блок до поляризации
    g = np.array([[1, 0], [1, 1]])
    G = g
    for i in range(n - 1):
        G = np.kron(G, g)  # Произведение кронекера

    answer = np.dot(U, G) % 2  # Блок после поляризации

    # print("Message:             ", msg)
    # print("Reliability sequence:", RS)
    # print("U:                   ", list(U))
    # print("answer:              ", list(answer))

    msg_file = open("message.txt", "w")
    msg_file.seek(0)
    msg_file.write("Message:         " + " ".join([str(i) for i in msg]) + "\n")
    msg_file.close()

    answer_BPSK = [1 - 2 * n for n in answer]
    BPSK_text = open("BPSK.txt", "w")
    BPSK_text.seek(0)
    BPSK_text.write(" ".join([str(i) for i in answer_BPSK]) + "\n")
    BPSK_text.close()

    for i in range(len(answer_BPSK)):
        if randint(0, 9) < int(E * 10):
            answer_BPSK[i] = int(sign(answer_BPSK[i]) * -1)

    BPSK_text = open("BPSK.txt", "a")
    BPSK_text.write(" ".join([str(i) for i in answer_BPSK]) + "\n")
    BPSK_text.close()


if __name__ == "__main__":
    encoder()
