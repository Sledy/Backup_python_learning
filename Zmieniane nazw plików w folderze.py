# Zmiana nazw plikow w folderze

# Importowanie bilbioteki systemowej

import os

''' Zmiana domyslnego katalogu gdzie operuje praogram na katalog na ktorym 
 chcemy pracowac. w ' ' umieszaczmy lokalizacje pliku ktora mozemy szybko uzyskac
 przerzucajac plik do konsoli windows '''

os.chdir('D:\Zdjęcia\Zdjęcia do Tapety')
print(os.getcwd())


'''os.listdir() Return a list containing the names of the entries in the
directory given by path'''

# Tworzenie zmiennej ktora bedzie nowa nazwa

licznik = 1

for f in os.listdir():
# (os.path.splitext(f)) funkcja rozdziela rozszerzenie od nazwy
    print()
    file_name, file_ext = os.path.splitext(f)
    if ('nr' in file_name):
        new_file_name = 'Fotografia Piotrka nr'
        new_name = '{0} {1}{2}'.format(new_file_name,licznik,file_ext)
        os.rename(f, new_name)  #Funckja zmienia nazwę pliku
        licznik += 1

    print ('Proces zakonczony')
    
