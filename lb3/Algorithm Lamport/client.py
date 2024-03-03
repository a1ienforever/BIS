import os
import random
from hashlib import sha256

# Процесс регистрации

# 1. Сервер и клиент договаривается о числе
N = 500

# 2. Клиент выбирает случайное число P большой размерности (128 бит и более) это и есть пароль:
# P = str(random.getrandbits(128))
P = '56325044938985299914518370882061979348'


def recursion_hashing(P, n, counter=0):
    if counter < n:
        counter += 1
        return recursion_hashing(sha256(P.encode()).hexdigest(), n, counter)

    return P


# 3. Клиент выполняет N раз рекурсивно криптостойкое хеширование H над числом P
hashed_P = recursion_hashing(P, N)

# 3. Передача полувшегося хэшированного пароля на сервер
print(hashed_P)  # e4a6f9702b1524bbe1ea493a0dce0afaba5a1ea5cd581a6b07790b5c9a38beff

# Процесс аутентификации

# 1. Клиент принимает число A = 1

A = 1
# 2. Клиент выполняет (N-A) раз хеширование над числом P
check_password = recursion_hashing(P, N - A)  # 1b85545c482faff36ebdccc3b745e1a9214ab03e3a3fac1de2ee611f0bbeba60

# 2. передает получившийся результат H^N-A(P) серверу
print(check_password) # 1b85545c482faff36ebdccc3b745e1a9214ab03e3a3fac1de2ee611f0bbeba60
