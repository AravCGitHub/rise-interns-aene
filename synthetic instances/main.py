import random
import numpy as np
import time
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression

def createSyntheticInstance(numAdvs, numImps):
    numTypes = 10
    advsList = []
    for i in range(numAdvs):
        advsList.append(Advertiser(numTypes))
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))
    return advsList, impsList

def createMatrixA(advs, imps):
    # Part 1: Advertiser Constraints
    matrixA = []
    for count in range(len(advs)):
        aList = []
        for i in range(len(advs)):
            if i == count:
                temp = [1.0] * len(imps)
                aList += temp
            else:
                temp = [0.0] * len(imps)
                aList += temp
        matrixA.append(aList)
    # Part 2: Impression Constraints
    zeroBefore = 0
    zeroAfter = len(imps)-1
    for i in range(len(imps)):
        temp = zeroBefore*[0.0] + [1.0] + zeroAfter*[0.0]
        zeroBefore += 1
        zeroAfter -=1
        temp *= len(advs)
        matrixA.append(temp)
    # Part 3: Weight Constraints
    zeroBefore = 0
    zeroAfter = len(imps)*len(advs)-1
    for i in range(len(imps)*len(advs)):
        temp = zeroBefore*[0.0] + [-1.0] + zeroAfter*[0.0]
        zeroBefore += 1
        zeroAfter -=1
        matrixA.append(temp)
    return matrixA

def createVectorB(advs, imps):
    vectorB = []
    budgetsList = []
    for bud in advs:
        budgetsList.append(bud.returnBudget())
    impressionsList = [1] * len(imps)
    advertisersList = [0] * (len(imps) * len(advs))
    vectorB = budgetsList + impressionsList + advertisersList
    return vectorB

def createVectorC(advs, imps):
    vectorC = []
    for a in advs:
        for i in imps:
            vectorC.append(-1*a.returnValuation()[i.returnType()])
    return vectorC

def lpSolve(advs, imps):
    npMatrixA = np.array(createMatrixA(advs,imps))
    npMatrixA.transpose()
    A = matrix(npMatrixA)
    npVectorB = createVectorB(advs,imps)
    B = matrix(npVectorB, (npMatrixA.shape[0], 1), 'd')
    C = matrix(createVectorC(advs, imps))
    startTime = time.time()
    sol = solvers.lp(C, A, B)
    endTime = time.time()
    return sol['x'], endTime - startTime

def objectiveValue(solved, vectorC):
    npSolv = np.array(solved).ravel()
    dot = np.dot(npSolv * -1, vectorC)
    return dot

def main():
    a, i = createSyntheticInstance(50,100)
    solved, timeTaken = (lpSolve(a,i))
    print(timeTaken)
    objVal = objectiveValue(solved, createVectorC(a,i))
    print(objVal)

main()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib
# objective value v impressions, time v impressions, comparing cvxopt and algo