import time
import os

dir = input("Write filepath: ")
if not os.path.isdir(dir):
    print("Wrong filepath.")
else:
    while True:
        file = input("Write filename: ")
        if os.path.isfile(os.path.join(dir, file)):
            print('The filename is correct')
            full_path = os.path.join(dir, file)
            print('Last modification: {}\nCreation time: {}\nAccess time: {}\nSize: {}B'.format(time.localtime(os.path.getmtime(full_path)),\
                                                                                               time.localtime(os.path.getctime(full_path)),\
                                                                                               time.localtime(os.path.getatime(full_path)),\
                                                                                               os.path.getsize(full_path)))
            break
        else:
            print("Wrong filename, try again: ")
