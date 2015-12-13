from decimal import *
import math
import threading
import time

#read the digits of pi from the givin text file
f = open('100000.txt', 'r')
pi = Decimal(f.read())
f.close()

def EulerPi(depth, digitsPrecision):
    getcontext().prec = digitsPrecision
    base = Decimal(0) #the number to be used to store the EulerPi ests
    for denom in range(1, depth + 1):#start at one and end at the depth inclusive of the depth
        base = base + (Decimal(1) / Decimal(denom**2))
    return Decimal.sqrt(6 * base)

def EulerPiThreaded(NumberOfThreads, depth, digitsPrecision):
    getcontext().prec = digitsPrecision
    length = depth // NumberOfThreads # the depth of calculation per thread
    firstLength = depth % NumberOfThreads + length # if depth does not divide the number of threads then this needs to be handled
    threads = []
    base = Decimal(0)
    currentIndex = 1
    currentThread = EulerPiThread(0,currentIndex, firstLength)
    currentThread.start()
    threads.append(currentThread)
    for thread in range(1, NumberOfThreads):
        currentThread = EulerPiThread(thread, thread * length + 1, length)
        currentThread.start()
        threads.append(currentThread)
    for thread in threads:#wait for all the threads to complete, then add their calculations to the base
        thread.join()
        base = base + thread.myBase
    return Decimal.sqrt(6 * base)
def EulerPiParts(start, length):
    #useful for threading. Start is the first denominator to be used, length is how many iterations this thrad will use
    base = Decimal(0)
    for denom in range(start, start + length):
        base = base + (Decimal(1) / (Decimal(denom) * Decimal(denom)))
    return base
class EulerPiThread (threading.Thread):
    def __init__(self, threadID, starting, length):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.length = length
        self.starting = starting
        self.myBase = Decimal(0)
    def run(self):
        self.myBase = EulerPiParts(self.starting, self.length)
def SerialPi(depth):
    aResults = [1,3,0]
    bResults = [1,4,0] #the base digits
    results = [4,3] # the base results
    for index in range(2, depth):
        #see the formula for generalized continued fractions computation
        a = index ** 2
        b = index * 2 + 1
        aResults[index % 3] = b*aResults[(index - 1) % 3] + aResults[(index - 2) % 3] * a
        bResults[index % 3] = b * bResults[(index - 1) % 3] + bResults[(index - 2) % 3] * a
        results.append(4 * (aResults[index % 3] / bResults[index % 3])) # 4*A/B is the current
    return results
def SerialPiPrecise(depth, digitsPrecision):
    #this method is identical to the SerialPi function except it uses decimals with a precision digitsPrecision
    getcontext().prec = digitsPrecision
    aResults = [Decimal(1), Decimal(3), Decimal(0)]
    bResults = [Decimal(1), Decimal(4), Decimal(0)]
    results = [4,3]
    indecies = []
    for index in range (2, depth):
        a = Decimal(index) * Decimal(index)
        b = Decimal(index) * 2 + 1
        aResults[index % 3] = b*aResults[(index - 1) % 3] + aResults[(index - 2) % 3] * a
        bResults[index % 3] = b * bResults[(index - 1) % 3] + bResults[(index - 2) % 3] * a
        results.append(4 * aResults[index % 3] / bResults[index % 3])
    return results
def OutOfDefinition():
    #take the results from serial pi and check to see if there is no difference
    #return the index of that occurance
    step = 50 #since reading values can be expensive we start by reading to depth 50
    last = 0 # a temp variable for the last value checked... what the estimate will be compared to
    stepCounter = 0 # how many steps we have made
    for index in range (1, 10000):
        stepCounter = 0 #reset the step conter
        results = SerialPi(step * index) #read up to step * index depth
        for currentIndex in range(step * (index -1), step * (index)):
            #start at the step * index -1 stepping index number of times
            est = results[currentIndex]
            if est == last: #check if they are equal
                return stepCounter
            stepCounter = stepCounter + 1 #increment the step counter
            last = est #swap the variables
def NumberOfSimDigit(a,b): # a is the longer number
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
def NToGetTo(target):
    index = 0
    majorStep = 10**(target - 1) #how much the initial jump is by
    direction = -1
    piEst = 0
    digits = 0

    while (digits < target): #jump around to find the 
        index = index + majorStep
        piEst = EulerPiThreaded(8, index, ((digits + 1)**2)*256)
        print(str(index) + ". " + str(piEst))
        digits = NumberOfSimDigit(pi, piEst)
    while (abs(majorStep) != 1):#a binary search
        majorStep = abs(majorStep) // 2 * direction
        index = index + majorStep
        piEst = EulerPiThreaded(8, index, ((digits + 1)**2)*256)
        print(str(index) + ". " + str(piEst))
        digits = NumberOfSimDigit(pi, piEst)
        if (digits >= target):
            direction = -1
        else:
            direction = 1
    if (digits == target):#we need to step down instead of up
        direction = -1
    while(digits != target):
        index = index + direction
        piEst = EulerPiThreaded(8, index, ((digits + 1)**2)*256)
        print(str(index) + ". " + str(piEst))
        digits = NumberOfSimDigit(pi, piEst)
    print (digits)     
    return index
def FindOptimal(ratio):
    currentRatio = 100
    num = 100
    while(currentRatio > ratio):
        num = num + 1
        timeStart = time.time()
        EulerPiThreaded(2, num, num)
        timeTaken = time.time() - timeStart
        #print(str(timeTaken) + " seconds to find the first num iterations of Euler Pi with two threads")
        currentRatio = timeTaken
        timeStart = time.time()
        EulerPi(num,num)
        timeTaken = time.time() - timeStart
        #print(str(timeTaken) + " seconds to find the first num iterations of Euler pi unthreaded")
        if (timeTaken != 0.0):
            currentRatio = currentRatio / timeTaken
    return num

#Question 1: "Eventually your approximation runs out of floating point resolution. At what value of n does serialpi stop changing?"print(OutOfDefinition())#22
#Question 2: "What n do you need to get 100 correct digits of pi? 1000 digits? 10000 digits?"
num = 15000 #limit of digits and depth
results = (SerialPiPrecise(num,num))
#create a CSV file
r = open(str(num) + "_Results.csv", 'w')
print("Calc complete")
#write the first
r.write(str(0) + "," + str(0) + "\n")
for index in range (1, len(results)):
    simDigits= NumberOfSimDigit(pi, results[index])
    r.write(str(index) + "," + str(simDigits) + "\n")
r.close() #close the writer
#130, 1306, 13062

#Question 3 - "What is the smallest n you need to get 6 correct digits of pi: 3.14159?"
print(NToGetTo(6))
#359612

#measure the time taken by each process.. just wrap the function call in time() and take their difference
num = 2500
timeStart = time.time()
SerialPiPrecise(num,num)
timeTaken = time.time() - timeStart
print(str(timeTaken) + " seconds to find the first num iterations of serial pi")

#Question 4: "Approximately how big does n have to be so that eulerpiparallel(n,2) takes 60% of the timeof eulerpi(n)?"
print(FindOptimal(.6))
#n ~= 943
