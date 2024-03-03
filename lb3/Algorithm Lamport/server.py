from hashlib import sha256
# Регистрация: пароль и логин отправить в бд
# 3. Сервер принимает хэшированный пароль H^N(P)
hashed_P = 'e4a6f9702b1524bbe1ea493a0dce0afaba5a1ea5cd581a6b07790b5c9a38beff'


# Аутентификация
# 1. Сервер высылает претенденту число A.
A = 1


def recursion_hashing(P, n, counter=0):
    if counter < n:
        counter += 1
        return recursion_hashing(sha256(P.encode()).hexdigest(), n, counter)

    return P


# 2. Сервер принимает H^N-A(P)
checked_P = "1b85545c482faff36ebdccc3b745e1a9214ab03e3a3fac1de2ee611f0bbeba60"

# 3. Сервер производит над числом H^N-A(P) еще A раз хеширование
hashed_P_2 = recursion_hashing(checked_P, A)

# Результат совпадает!
print(hashed_P_2) # e4a6f9702b1524bbe1ea493a0dce0afaba5a1ea5cd581a6b07790b5c9a38beff