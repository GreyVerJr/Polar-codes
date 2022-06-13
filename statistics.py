from decoder import decoder
from encoder import encoder
from parameters import *
import time


f = open('statistics.txt', 'w')
f.close()

counter = 0
start_time = time.time()
for i in range(number_of_tests):
    encoder()
    decoder()

    BPSK_file = open("message.txt", "r")
    file = BPSK_file.read().split("\n")
    BPSK_file.close()
    message = file[0][17:].split(" ")
    decoded_message = file[1][17:].split(" ")
    is_result_correct = message == decoded_message
    if not is_result_correct:
        stat_file = open("statistics.txt", "a")
        stat_file.write(file[0] + "\n")
        stat_file.write(file[1] + "\n" * 2)
        stat_file.close()
        counter += 1

print("\nВероятность ошибки: %s" % E)
print("Длина блока: %s" % N)
print("Длина сообщения: %s" % K)
print("Количество неудачных декодирований: " + str(counter) + "/" + str(number_of_tests))
print("Время выполнения программы секундах: %s" % round((time.time() - start_time), 4))
