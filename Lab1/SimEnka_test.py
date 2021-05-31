import time
from SimEnka_testing_edition import *
start_time = time.time()
valid = 0
for i in range(1, 54):
    folder = "test"
    if i < 10:
        folder += "0"
    folder += str(i)
    a = main(f"./lab1_primjeri[1]/{folder}/test.a")
    b = open(f"./lab1_primjeri[1]/{folder}/test.b").read()
    if a == b:
        print("Test " + str(i) + ": uspješno, vrijeme je " + str(time.time()-start_time))
        start_time = time.time()
        valid += 1
    else:
        print("Test " + str(i) + ": neuspješno, vrijeme je " + str(time.time()-start_time))
        print(a)
        print(b)
        start_time = time.time()
print(f"{valid}/33")