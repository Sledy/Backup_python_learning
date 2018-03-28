# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 19:08:53 2017

@author: Adam
"""

def write_func(file_read,file_write):
    for line in file_read:
        if ('Hint' in line):
            break
        file_write.write(line)
    return None

with open("Zadania python.txt", 'r') as plik:
    with open("Nowy plik.txt",'w') as dok:
        counter = 1
        for line in plik:
            if ('Question:' in line):
                dok.write(f"Question: {counter} \n")
                counter += 1
                write_func(plik, dok)
                continue
            
                
                


        
                
            
                
                    