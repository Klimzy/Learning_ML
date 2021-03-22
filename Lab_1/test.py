import random
import graycode
import math

def dc_to_gray(number):
    return '{:09b}'.format(graycode.tc_to_gray_code(number))

def muatation (chromosome):
    print('5')




def fitness(chromosome):
    y = 0.0
    y = (0.8 * math.cos(3 * chromosome) + math.cos(chromosome)) * (chromosome - 4)
    return round(y, 4)

a = []
for i in range(0, 10):
    a.append('{:09b}'.format(graycode.tc_to_gray_code(i)))
print(a)


a = [graycode.gray_code_to_tc(int(a[i], 2)) for i in range(0, len(a))]

print(a)
