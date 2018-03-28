from itertools import chain, combinations
from random import randint
import datetime
import numpy as np

class StringValidatation:

    @staticmethod
    def is_valid_parenthese(str1):
        stack, pchar = [], {"(": ")", "{": "}", "[": "]"}
        for parenthese in str1:
            if parenthese in pchar:
                stack.append(parenthese)
            elif len(stack) == 0 or pchar[stack.pop()] != parenthese:
                return False
        return len(stack) == 0

class UniqueSubsets:

    def powerset(self, argument):
        s = list(argument)

        return list(chain.from_iterable(combinations(s,r) for r in range(len(s)+1)))

#print(UniqueSubsets().powerset([1,2,3]))

class Element_finder:
    
    def find(self, array, target):
        for i in range(len(array)):
            try:
                if (array[i] + array[i+1]) == target:
                    return (array[i],array[i+1])
            except IndexError:
                break

#lista = [1,2,4,5,10,20,30,40,50,60,70,80]
#print(Element_finder().find(lista, 50))

class ZeroSet:

    @staticmethod
    def find(argument):
        result_list = []
        for element1 in argument:
            for element2 in argument:
                if element2 == element1:
                    continue
                else:
                    for element3 in argument:
                        if element3 == element2 or element3==element1:
                            continue
                        else:
                            if element1 + element2 + element3 == 0:
                                temp =[element1,element2,element3]
                                temp.sort()
                                if  temp not in result_list:
                                    result_list.append(temp)
                            else:
                                continue
        print(result_list)

    def threeSum(self, nums):
        nums, result, i = sorted(nums), [], 0
        while i < len(nums) - 2:
            j, k = i + 1, len(nums) - 1
            while j < k:
                if nums[i] + nums[j] + nums[k] < 0:
                    j += 1
                elif nums[i] + nums[j] + nums[k] > 0:
                    k -= 1
                else:
                    result.append([nums[i], nums[j], nums[k]])
                    j, k = j + 1, k - 1
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1
                    while j < k and nums[k] == nums[k + 1]:
                        k -= 1
            i += 1
            while i < len(nums) - 2 and nums[i] == nums[i - 1]:
                i += 1
        return result
class NumberPower:

    @staticmethod
    def compute(input_number,power):
        return input_number**power

class Reverse_word:

    @staticmethod
    def build(word):
        temp = word.split()
        temp.reverse()
        print(' '.join(temp))


def fibonacii(maximal):
    lista = []
    i, j = 0,1
    lista.append(i)
    lista.append(j)
    while i+j<(maximal):
        i, j = j, i+j
        lista.append(j)
    lista = list(filter(lambda x: x%2==0, lista))
    print(sum(lista))


def PrimeFactor(number):
    i = 1
    while i<=number:
        k = 0
        if number%i==0:
            j=1
            while j<=i:
                if i%j==0:
                    k +=1
                j+=1
            if k==2:
                print(i)
        i+=1


def Polindrome():
    flag = []
    for i in range(100,1000):
        for j in range(100,1000):
            if(str(i*j) == str(i*j)[::-1]):
                flag.append(i*j)
    return flag

def SmallestMultiple():
    i= 1
    dividers = [j for j in range(2,21)]
    while True:
        print(i)
        if all( i%element==0 for element in dividers):
            break
        i+=1
#SmallestMultiple()

def sum_squares(limit):
    #sum of sguares:
    sum_sq = 0
    #square of sums:
    sq_sum = 0
    for i in range(limit):
        sum_sq += i**2
        sq_sum += i
    sq_sum = sq_sum**2
    print(sq_sum, sum_sq, sq_sum-sum_sq)
#sum_squares(101)

def only_prime(limit):
    number = 2
    counter = 0
    while True:
        dividers = 0
        #Idziemy po wszystkich liczbach mniejszych od number
        for i in range(1, number+1):
            if (number%i==0):
                dividers += 1
                if dividers > 2:
                    break
        if dividers == 2:
            #print (number)
            counter += 1
        if counter == limit:
            print ("Zanalazlo {} liczb".format(counter))
            print ('{} liczba pierwsza to {}'.format(counter, number))
            break
        print (counter)
        number += 1
#only_prime(10001)

def adjacent_numbers():
    given_number = '''7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'''
    flag = 1
    product_list = []
    for i in range(len(given_number)):
        try:
            for j in range(i,i+13):
                flag = flag * int(given_number[j])
            product_list.append(flag)
        except IndexError:
            break
        flag = 1
    print(max(product_list))

def pythagorean_triplet():
    for k in range(1000):
        for j in range(1000):
            if (j >= k):
                break
            for i in range(1000):
                if (i>=j):
                    break
                if (i**2+j**2==k**2) & (i+j+k == 1000):
                    suma = i + j + k
                    print(i,j,k)
                    print(i*j*k)


def sum_prime(limit):
    prime_list = []
    sum_list = []
    for number in range(2, limit):
        boolean_flag = True
        for divider in prime_list:
            if (number % divider == 0):
                boolean_flag = False
                break
        if boolean_flag == True:
            print ('Liczba pierwsza: {}'.format(number))
            prime_list.append(number)
    #print(prime_list)
    print(sum(prime_list))




def adjacent_numbers_matrix ():
    matrix = []
    with open('New Text Document.txt', 'r') as file:
        for row in file:
            matrix.append(row.strip('\n').split(' '))
    matrix = np.array(matrix)
    width, height = matrix.shape
    matrix = matrix.astype(int)
    horizontal_sum =[]
    max_list = []
    #Horizontally
    for row in range(height):
        for column in range(width-3):
            horizontal_sum.append(matrix[row][column]*matrix[row][column+1]*matrix[row][column+2]*matrix[row][column+3])
    print(max(horizontal_sum))
    #Vertical
    vertical_sum = []
    for column in range(width):
        for row in range(height-3):
            vertical_sum.append(matrix[row][column] * matrix[row+1][column] * matrix[row+2][column] * matrix[row+3][column])
    print(max(vertical_sum))
    #Diagonal
    diagonal = []
    for row in range(height):
        for column in range(width):
            try:
                #print(matrix[row][column], matrix[row + 1][column+1],matrix[row + 2][column+2], matrix[row + 3][column+3])
                diagonal.append(matrix[row][column] * matrix[row + 1][column+1] * matrix[row + 2][column+2] * matrix[row + 3][column+3])
            except:
                break
    print(max(diagonal))
#adjacent_numbers_matrix()

