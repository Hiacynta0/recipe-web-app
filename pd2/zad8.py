import os

my_list = ['blue','red','yellow','pink','green']
my_string = 'Some words to fill the string'
address = input("Write your favorite site address: ")
filepath = 'D:/Studia/Semestr4/JSkryptowe/Python/pd2/test.txt'

with open(filepath, 'w') as file:
    for color in my_list:
        file.write(color + '\n')
    file.writelines(my_string)

# with open('C:\\Scripts\\New_file.py', 'r') as file:
#     for line in file:
#         print(line)
#
# with open('C:\\Scripts\\New_file.py', 'a') as file:
#     file.write('\n')
#     file.write("Hello, It's a new fragment.")
#
# with open('C:\\Scripts\\New_file.py', 'r') as file:
#     for line in file:
#         print(line)