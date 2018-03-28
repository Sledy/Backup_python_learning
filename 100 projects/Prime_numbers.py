# This function return n prime numbers

def prime_generator(quantity):
    flag, inspect_number = 0, 2
    prime_list = []

    while flag < quantity:
        bool_flag = True


        for divider in prime_list:
            if inspect_number % divider == 0:
                bool_flag = False
                break


        if bool_flag:
            flag += 1
            prime_list.append(inspect_number)

        inspect_number += 1

    return prime_list

quantity = int(input('Please, specify quantity of prime numbers you want: '))
print(prime_generator(quantity))