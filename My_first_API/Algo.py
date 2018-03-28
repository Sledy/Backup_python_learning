import random


array  = [random.randint(-1000,1000) for i in range(100000)]

for i in range(len(array)):
    if (sum(array[0: i]) == sum(array[i+1: len(array)-1])):
        print (i)
        break

