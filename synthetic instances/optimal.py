import numpy as np
import time
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt

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
    return np.array(sol['x']).ravel(), endTime - startTime