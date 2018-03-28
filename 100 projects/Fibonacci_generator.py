def fibonacci(amount):
    a, b = 0, 1
    flag = 0

    while flag <= amount:
        yield (a)
        flag += 1
        a, b = b, a + b


number = int(input('Specify, how many number from Fibonacci seqeunce you want to see: '))
print(list(fibonacci(number)))