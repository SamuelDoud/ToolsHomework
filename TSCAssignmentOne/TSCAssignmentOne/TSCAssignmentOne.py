import math
import decimal
from decimal import *
def EulerPi(depth):
    approx = 0
    for index in range(0,depth):
        approx = approx + 6 * math.pow(index+1,-2)
    return math.sqrt(approx)
def serialPi(depth):
    reverseIndex = depth
    current = 0.0
    for index in range(0,depth):
        reverseIndex = depth - index
        current = reverseIndex * reverseIndex / (reverseIndex * 2 + 1 + current)
    return 4/(current + 1.0)
def serialPiPrecise(depth, precision):
    decimal.getcontext().prec = precision
    A = [Decimal(1),Decimal(3),Decimal(0)]
    B = [Decimal(1),Decimal(4),Decimal(0)]
    result = [Decimal(4),Decimal(3)]
    index = Decimal(2)
    while index < Decimal(depth):
        a = index*index
        b = index * 2 + 1
        intIndex = int(index)
        A[intIndex %3] = b*A[(intIndex-1) %3]+A[(intIndex-2) %3]*a
        B[intIndex %3] = b*B[(intIndex-1) %3]+B[(intIndex-2) %3]*a
        result.append(4*(A[intIndex%3]/B[intIndex%3]))
        #print(index)#simply track the index we are on. Debugging purposes
        index = index + Decimal(1)
    return result
#calculates the point at which the serial Pi function runs out of bit resolution
def serialPiOutOfRes():
    first = serialPi(0)
    second = 0
    count = 1
    while (first != second):
        first = second
        second = serialPi(count)
        count = count + 1
    return count
def NumberOfSimDigit(a,b):
    strA = str(a)
    strB = str(b)
    minLen = len(strB)
    if (minLen > len(strA)):
        minLen = len(strA)
    countSim = 0
    for index in range(0,minLen):
        if strA[index] == strB[index]:
            if strA[index] != '.':
                countSim=countSim+1
        else:
            return countSim
    return countSim
f = open('100000.txt', 'r')
pi = Decimal(f.read())
f.close()
r = open("result.csv", 'w')
print (pi)
print(serialPiOutOfRes())
num = 1500
results = (serialPiPrecise(num,num))
print(results[num -1])
print("Calc complete")
print(NumberOfSimDigit(1.1234, 1.1235))
for index in range (0, len(results)):
    simDigits= NumberOfSimDigit(pi, results[index])
    r.write(str(index) + "," + str(simDigits) + "\n")
    if (simDigits == 100):
        print (str(index) + ". " + str(simDigits))
r.close()