import math
import decimal


class DecimalError(Exception):

    def __init__(self):
        print('Decimal numbers cannot exceed 50')

def e_number(decimal_numbers):

    if decimal_numbers > 50:
        raise DecimalError

    e = math.e

    pi = str(decimal.Decimal(e))

    return pi[:decimal_numbers+2]

decimal_number = int(input('Please specify decimal numbers: '))

print(e_number(decimal_number))