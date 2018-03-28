# Question 1

'''
def finding_function():
    for i in range(2000,3201):
        if ((i%7==0)and(i%5 != 0)):
            yield str(i)

print ('.'.join(finding_function()))
'''

#Question 2:

'Recursion'

'''
def factorial(base):
    if (base==1):
        return 1
    else:
        return base*factorial(base-1)
print(factorial(8))
'''


#Question 3

'''
def dictionary_creator(i):
    dictionary = {x: x**2 for x in range (1,i+1)}
    print (dictionary)

dictionary_creator(8)
'''

#Question 4

'''
sequence_given = '34,67,55,33,12,98'
def task(sequence):
    lista = sequence_given.split(',')
    tuplecik = tuple (lista)
    print(lista, tuplecik)

task(sequence_given)

'''
#Question 5
'''
class InputOutString():

    def getString(self):
        self.s = input("Proszę wpisać dane")

    def printString(self):
        print (self.s.upper())

strObj = InputOutString()
strObj.getString()
strObj.printString()
'''
#Question 6
'''
from math import sqrt

argument = '100,150,180'
def custom_calc(arg):
    C = 50
    H = 30
    sequence = list(arg.split(','))
    wynik = []
    for D in sequence:
        D = int(D)
        wynik.append(int(sqrt((2*C*D)/H)))
    return wynik

print (custom_calc(argument))
'''

#Question 7


'TWORZENIE MACIERZY'
'''
def array_generator ():
    row, col = input('Wprowadz wartosci oddzielajac je spacją: ').split(' ')
    print (row+' i '+col)
    row = int(row)
    col = int(col)
    array = [[0 for coluumn in range(col)] for row in range(row)]
    for x in range(row):
        for y in range(col):
            array [x][y] = x*y
    print (array)
    return array
    
array = array_generator()
print (type(array[0][0]))

import numpy as np
import random
row = 5
column = 6
'''
'''
macierz = [[0 for i in range(column)] for i in range(row)]


for row in range(row):
    for column in range(column):
        macierz[row][column] = random.randint(1,10)
print (macierz,'\n')
print (2*macierz)

macierz = np.array(macierz)
print ('\n', 2*macierz)
'''
#Question 8
dana = 'without,hello,bag,world'
'''
def sorting(string):
    dana = list(string.split(','))
    dana = sorted(dana)
    dana = ','.join(dana)
    print (dana)
    
sorting(dana)
'''
#Question 9
'''
dana = 'hello world and practice makes perfect and hello world again'

def simple_sort(arg):
    dana = arg.split(' ')
    dana = set(dana)
    print (dana)
    dana = sorted(dana)
    dana = ' '.join(dana)
    return dana

print (simple_sort(dana))
'''
#Question 10
'''
number = '0100,0011,1010,1001'

def binary_division (number):
    lista = number.split(',')
    lista2 = []
    for i in lista:
        print (i)
        i = int(i,2)
        print(i)
        if (i%5==0):
            i = bin(i)
            i = str(i)
            lista2.append(i)
    
    dana = ','.join(lista2)
    print (dana)
    print(type(dana))
    dana.strip('b')
    print (dana)      

binary_division(number)
'''

#Question 12
'''
lista = []

for i in range (1000,3001):
    i = str(i)
    if (('1' not in i )and('3' not in i )and('5' not in i )and('7'not in i )and('9'not in i )):
        lista.append(i)
        
print(lista)
'''

#Question 13
'''
wejscie = 'Hello world!'

def counter(wyraz):
    Count_up = 0
    Count_low = 0
    for i in wyraz:
        print (i)
        if (i.isupper()):
            Count_up += 1
        elif (i.islower()):
            Count_low +=1
    print (f"Duże litery: {Count_up} oraz małe litery {Count_low}")

counter(wejscie)
            
'''

#Question 14
'''
def calc(arg):
    wynik = 1*arg+11*arg+111*arg+1111*arg
    print (wynik)
calc(5)
'''

#Question 15
'''
lista = '1,2,3,4,5,6,7,8,9'

def moderator(arg):
    lista = [str(int(i)**2) for i in arg.split(',') if (int(i)%2!=0)]
    print(lista)
    print (','.join(lista))

moderator (lista)
'''

#Question 16
'''

def bank_log():
    net = 0
    while True:
        string = input()
        if not string:
            break
        values = string.split(' ')
        operation = values[0]
        if (operation=='D'):
            net += int(values[1])
        elif (operation=='W'):
            net -= int(values[1])
        else:
            break
    print (net)
            
bank_log()        

'''
#Question 17
'''
import re



password = 'ABd1234@1,a F1#,2w3E*,2We3345'



def secure_check(password):
    lista = password.split(',')
    for i in lista:
        if (not re.search('[a-z]',i)):
            print ('Haslo nie zawiera malej litery!')
            continue
        elif (not re.search('[A-Z]',i)):
            print ('Haslo nie zawiera wielkiej litery!')
            continue
        elif(not re.search('[1-9]',i)):
            print ('Hasło nie zawiera cyfr!')
            continue
        elif(not(re.search('[$#@]',i))):
            print ("Nie zaweira $#@")
            continue
        elif(len(i)<6)or(len(i)>12):
             print('Nieodpowiednia długosc hasla')
             continue
        print (i)
        
secure_check(password)

'''
#Question 18
'''
from operator import itemgetter
print ("Please write data in the following order and manner: 'Name,Age,Score'\n")
lista = []
while True:
    new_tuple = input()
    if (new_tuple == ''):
        break
    lista.append(tuple(new_tuple.split(',')))
    
lista = sorted(lista, key = itemgetter(0,1,2))
print (lista)
'''

#Question 19
'''

#Porownanie generatora i zwyklej petlli (generator duzo szybszy)
import time
def generator(n):
    for i in range(n):
        if (i%7==0):
            yield i
 


start_time = time.time()


for i in generator(1000000):
    print (i)
execute_time1 = time.time() - start_time
print ('Pierwsza operacja: {}'.format(execute_time1))

start_time = time.time()
for i in range (100000):
    print (i)
execute_time2 = time.time() - start_time
print ('Druga operacja: {}'.format(execute_time2))

with open("czasomierz.txt", 'w') as file:
    file.write(str(execute_time1) +'\n'+ str(execute_time2))
'''

#Question 20
'''
from math import sqrt

gora = 0
dol = 0
lewo = 0
prawo= 0
while True:
    temp = input()
    if (temp==''):
        break
    kierunek, wartosc = temp.split(' ')
    wartosc = int(wartosc)
    if (kierunek == 'UP'):
        gora += wartosc
    elif (kierunek == "DOWN"):
        dol += wartosc
    elif (kierunek == "LEFT"):
        lewo += wartosc
    elif (kierunek == "RIGHT"):
        prawo += wartosc
#Koncowe rachunki
horizontal = prawo - lewo
vertical = gora - dol
odleglosc = sqrt(horizontal**2 + vertical**2)
print (f"Gora {gora}, Dol {dol}, Lewo {lewo}, Prawo {prawo}")
print (f"Odległosc wynosi {odleglosc}")
'''
#Question 21
'''
dany_string = 'New to Python or choosing between Python 2 and Python 3? Read Python 2 or Python 3.'
frequency = {}
print (type(frequency))
for word in dany_string.split():

    frequency [word] = frequency.get(word,0)+1

word = list(frequency.keys())
word.sort()

for w in word:
    print ("{0}:{1}".format(w,frequency[w]))
'''
#Question 22
'''
def square (arg):
    return arg**2
'''
#Question 23

'''
class Person:
    name = 'Person'
    
    def __init__(self,name,last):
        self.name = name
        self.last = last


adam = Person("Adam",'Śledziewski')
print (f'{Person.name} name is {adam.name} and last name is {adam.last}')

krzysie= Person("Krzyszof", "Rytel")
print (f'{Person.last} name is {krzysie.name} and last name is {krzysie.last}')
'''

#Question 24
'''
def dict_generator (m):
    dictionary = {i: i**2 for i in range(1,m+1)}
    for i in range (1,m+1):
        print (dictionary[i])
dict_generator (10)
'''
#Question 25
'''
def dict_generator (m):
    dictionary = {i: i**2 for i in range(1,m+1)}
    for k in dictionary.keys():
        print (k)
dict_generator(20)
'''
#Question 

