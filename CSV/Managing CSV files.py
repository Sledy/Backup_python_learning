# Praca z plikami w fomrmacie CSV. Przed uzyciem skomentuj jeden z blokow

#Imprort bibliotkei CSV
'''
import csv

#otwarcie pliku w Trybie "read"
with open('Zeszyt1.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ';')
    
    #Otwieramy plik, w ktorym zapiszem zedytowane dane z w/w pliku
    with open('Odzielone tab.csv', 'w') as new_file:
       
        # tworzymy zmienna zapisujaca w pliku dane
        # funckja csv.writer(nazwa pliku gdzie pracujemy, znak ktorym chcemy
        # oddzielic wyrazy)
        # '\t' oznacza odstep za pomoca tabulatora
        csv_writer = csv.writer(new_file, delimiter='\t')
        
        for line in csv_reader:
            csv_writer.writerow(line)
 '''           
       

# Gdy chcemy by nasz plik operowal na slownikach uzywamy kodu ponizej

import csv

with open('Zeszyt1.csv', 'r') as csv_file2:
    csv_reader2 = csv.DictReader(csv_file2, delimiter = ';')
    
    with open('Nowy plik.csv', 'w') as new_file2:
        field_names = ['first_name', 'last_name', 'email']
        
        csv_writer = csv.DictWriter(new_file2, fieldnames = field_names, delimiter = '\t')
        
        csv_writer.writeheader()
        
        for line in csv_reader2:
            csv_writer.writerow(line)
