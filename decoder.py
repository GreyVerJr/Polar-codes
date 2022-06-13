import numpy as np

from encoder import calc_rs
from parameters import *


def decoder():
    def xor(u1, u2):
        answer = []
        for i in range(len(u1)):
            answer.append((u1[i] + u2[i]) % 2)
        return answer

    def f_func(r):
        f = []
        r_len = len(r)
        for i in range(r_len // 2):
            f.append(np.sign(r[i]) * np.sign(r[i + r_len // 2]) * min(abs(r[i]), abs(r[i + r_len // 2])))
        return f

    def g_func(r, u):
        g = []
        r_len = len(r)
        for i in range(r_len // 2):
            g.append(r[i + r_len // 2] + (1 - 2 * u[i]) * r[i])
        return g

    def decode(r, depth, l=None):
        global index
        if l is None:
            l = r
        if depth == n:
            if index in frozen:
                index += 1
                return [0]
            else:
                if l[0] < 0:
                    index += 1
                    return [1]
                else:
                    index += 1
                    return [0]

        left_response = decode(r=r[:len(r) // 2], depth=depth + 1, l=f_func(l))
        right_response = decode(r=r[len(r) // 2:], depth=depth + 1, l=g_func(l, left_response))
        return xor(left_response, right_response) + right_response

    BPSK_text = open("BPSK.txt", "r")
    R = [int(i) for i in BPSK_text.read().split("\n")[1].split(" ")]
    BPSK_text.close()
    RS = []
    for i in reliability_sequence:
        if i < N:
            RS.append(i)
    frozen = [RS[i] for i in range(len(RS) - K)]
    global index
    index = 0
    U = decode(R, 0)
    U = np.array(U)  # Блок до поляризации
    g = np.array([[1, 0], [1, 1]])
    G = g
    for i in range(n - 1):
        G = np.kron(G, g)  # Произведение кронекера
    answer = np.dot(U, G) % 2

    msg = []
    for i in range(N):
        if RS[i] in frozen:
            continue
        msg.append(answer[RS[i]])

    # print("frozen: ", frozen)
    # print("R:      ", R)
    # print("RS:     ", RS)
    # print("result: ", result)
    # print("Message:", msg)

    file = open("message.txt", "a")
    file.write("Decoded message: " + " ".join([str(i) for i in msg]) + "\n")
    file.close()


if __name__ == "__main__":
    decoder()

