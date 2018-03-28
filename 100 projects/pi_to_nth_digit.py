# This program is aim to display pi number to nth digit
# Equation: Bellard's formula


import math
import decimal


class DecimalError(Exception):

    def __init__(self):
        print('Decimal numbers cannot exceed 50')

def pi_number(accuracy, decimal_numbers):

    if decimal_numbers > 50:
        raise DecimalError

    pi = 0

    for n in range(accuracy):
        pi += ((-1) ** n / (2 ** (10 * n))) * ( -2 ** 5 / (4 * n + 1) - 1 / (4 * n + 3) + 2 ** 8 / (10 * n + 1) -
                                                 2 ** 6 / (10 * n + 3) - 4 / (10 * n + 5) - 4 / (10 * n + 7) +
                                                 1 / (10 * n + 9))
    pi = (pi*(1/2**6))

    pi = str(decimal.Decimal(pi))

    return pi[:decimal_numbers+2]

accuracy = int(input('Please input accuracy order: '))
decimal_number = int(input('Please specify decimal numbers: '))

print(pi_number(accuracy, decimal_number))