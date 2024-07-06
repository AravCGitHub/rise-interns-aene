import math
from cvxopt import matrix, solvers
import numpy as np
import random
from advertiser import Advertiser
from impression import Impression

# def clamp(n, min, max): 
#     if n < min: 
#         return min
#     elif n > max: 
#         return max
#     else: 
#         return n 

def syntheticInstance(numAds, numImps):
    numTypes = 8
    ads = []
    for i in range(numAds):
        ads.append(Advertiser(numTypes))
    imps = []
    for i in range(numImps):
        sections = (6.0 / numTypes)
        rand = random.gauss(0,1) + 3
        type = random.randint(0, numTypes-1)
        # clamp(math.floor(0.5 + (rand / sections)), 1, numTypes)
        imps.append(Impression(type))
    return ads, imps

a, i = syntheticInstance(2,2)

budgetsArr = []
for x2 in a:
    budgetsArr.append(x2.returnBudget())

def createMatrixB(budgets, imps, ads):
    impressionsArr = [1] * imps
    advertisersArr = [0] * (imps * ads)
    return budgetsArr + impressionsArr + advertisersArr

# print(createMatrixB(budgetsArr, 3, 5))


def createMatrixC(imps, ads):
    matrixC = []
    for a in ads:
        for i in imps:
            matrixC.append(-1*a.returnValuation()[i.returnType()])

    return matrixC

# for j in a:
#     print(j)

# for k in i:
#     print(k.returnType())

def createMatrixA(imps, ads):
    matrixA = []
    for count in range(len(ads)):
        aArr = []
        for i in range(len(ads)):
            # currAd += 1
            if i == count:
                temp = [1.0] * len(imps)
                aArr += temp
            else:
                temp = [0.0] * len(imps)
                aArr += temp
        matrixA.append(aArr)

    zeroBefore = 0
    zeroAfter = len(imps)-1
    for i in range(len(imps)):
        temp = zeroBefore*[0.0] + [1.0] + zeroAfter*[0.0]
        zeroBefore += 1
        zeroAfter -=1
        temp *= len(ads)
        matrixA.append(temp)

    zeroBefore = 0
    zeroAfter = len(imps)*len(ads)-1
    for i in range(len(imps)*len(ads)):
        temp = zeroBefore*[0.0] + [-1.0] + zeroAfter*[0.0]
        zeroBefore += 1
        zeroAfter -=1
        matrixA.append(temp)
    return matrixA

npListA = np.array(createMatrixA(i, a))
npListA.transpose()
A = matrix(npListA)

npListB = createMatrixB(budgetsArr, len(i), len(a))
print(npListB)
# npListB.transpose()
# print(npListB)
# B = matrix(npListB)
B = matrix(npListB, (8, 1), 'd')
# print(B)

# print(A)

C = matrix(createMatrixC(i, a))
# print(C)

# print("C size:", C.size)
# print("A size:", A.size)
# print("B size:", B.size)

sol = solvers.lp(C, A, B)
print(sol['x'])

#make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib
#objective value v impressions, time v impressions, comparing cvxopt and algo 
