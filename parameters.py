from math import log2

index = 0
E = 0.2  # Вероятность ошибки
N = 512  # Длина блока
K = 100  # Длина сообщения
n = int(log2(N))
number_of_tests = 100
