import numpy as np
import nistrng
import random


class LCG:
    def __init__(self, a, c, m, seed):
        self.a = a
        self.c = c
        self.m = m
        self.seed = seed



    def rand_digit(self, n):
        size = 10
        with open('../Nums.txt', 'w') as file:
            for _ in range(n):
                self.seed = (self.a * self.seed + self.c) % self.m
                print(self.seed)
                res = self.seed
                res = str(bin(res)[2:12])
                if len(res) < size:
                    res = (size - len(res)) * '0' + res
                file.write(str(res) + '\n')


a = 1_664_525
c = 1_013_904_223
n = 2 ** 16
seed = 2

lcg = LCG(a, c, n, seed)

result = lcg.rand_digit(100000)
