# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 15:36:26 2017

@author: Adam
"""

import pandas as pd
from random import randint
import numpy as np

x,y = 5,4
lista = [i for i in range(10)]
print (lista)

lista1= [randint(1,10) for i in range(11)]
lista2 = [randint(1,10) for i in range(11)]
lista3 = [[ 0 for i in range(x)] for j in range(y)]
print (lista3)

for i in range(x-1):
    for j in range (y-1):
        lista3[i][j]=randint(1,5)
print (lista3)



lista4 = [i*j for i in range(10) for j in range(10)]
print (lista4)