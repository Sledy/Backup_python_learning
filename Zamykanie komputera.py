# Shutting down the computer

import os

print ("""Ten program służy do wyłączenia komputera komendą 'shutdown' \n""")
print ('Wpisz "a" jeśli chcesz przerwać automatyczne wyłączanie')
time_hour = input("Wprowadź liczbę godzin, po ktorej komputer zostanie zamkniety, aby wyjsć wybierz ENTER: ")

if (time_hour != 'a'):
    time_hour = float(time_hour)
    time_second = time_hour * 3600
    time_second = int(time_second)
    os.system("shutdown -s -t {}".format(time_second))
    print ("System zostanie zamknięty po {}h\n".format(time_hour))
    flag = input ("Wpisz 'a' i ENTER, aby anulowac procedure. /n Wcisnij ENTER by zakończyć:  ")
    if (flag == 'a'):
        os.system("shutdown /a")
        input ("Procedura anulowana. Wcisnij ENTER by zakończyć")
    else:
        None

else:
    os.system("shutdown /a")
    print('Automatyczne wyłączenie przerwane.')


