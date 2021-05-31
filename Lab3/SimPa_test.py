import time
from SimPa_TestingEdition import *
start_time = time.time()
valid = 0
for i in range(1, 26):
    folder = "test"
    if i < 10:
        folder += "0"
    folder += str(i)
    try:
        a = main(f"./primjeri/{folder}/primjer.in")
        b = open(f"./primjeri/{folder}/primjer.out").read()
        if a == b:
            print("Test " + str(i) + ": uspješno, vrijeme je " + str(time.time()-start_time))
            start_time = time.time()
            valid += 1
        else:
            print("Test " + str(i) + ": neuspješno, vrijeme je " + str(time.time()-start_time))
            print('Tvoje rjesenje je:\n', a)
            print('Njihovo rjesenje je:\n', b)
            start_time = time.time()
    except:
        print('Primjer {} je sjeban'.format(i))
print(f"{valid}/25")