import time
import numpy as np
import math

def calculateD(weight, lam):
    D = math.e ** (weight / lam - 1)
    return D

def minInd(arr):
    first = True
    min = 0
    minIndex = 0
    for i in range(len(arr)):
        if first == True and arr[i] != 0:
            minIndex = i
            min = arr[i]
            first = False
        elif (arr[i] < min and arr[i] != 0):
            min = arr[i]
            minIndex = i
    return minIndex

def solve(advs, imps, weights, lam = 0.25, eps = 0.21, numRounds = 50):
    xMatrix = np.zeros((len(advs), len(imps)))
    priorityScores = [(1+eps) ** -numRounds] * len(advs)
    startTime = time.time()
    for r in range(numRounds):
        # Step 1
        for i in range (len(imps)):
            sum = 0
            for a in range (len(advs)):
                D_a = calculateD(weights[a*len(imps)+i], lam)
                sum += priorityScores[a] * D_a
            for a in range (len(advs)):
                if (sum <= 1):
                    xMatrix[a][i] = priorityScores[a] * calculateD(weights[a*len(imps)+i], lam)
                else:
                    xMatrix[a][i] = (priorityScores[a] * calculateD(weights[a*len(imps)+i], lam)) / sum
        # Step 2
        for a in range (len(advs)):
            alloc = xMatrix[a].sum()
            if (alloc <= (advs[a].budget) / (1 + eps)):
                priorityScores[a] = (1 + eps) * priorityScores[a]
            if (alloc >= (advs[a].budget) * (1 + eps)):
                priorityScores[a] = priorityScores[a] / (1 + eps)
    # Final Check
    difList = []
    for a in range (len(advs)):
        if (xMatrix[a].sum() > advs[a].budget):
            # print("Check Adv:",a)
            valList = []
            difList.append(xMatrix[a].sum() - advs[a].budget)
            for i in range (len(imps)):
                valList.append(weights[a*len(imps) + i] * xMatrix[a][i])
            while (xMatrix[a].sum() > advs[a].budget):
                minIndex = minInd(valList)
                dif = xMatrix[a].sum() - advs[a].budget
                if (xMatrix[a][minIndex] > dif):
                    xMatrix[a][minIndex] -= dif
                else:
                    xMatrix[a][minIndex] = 0
                valList[minIndex] = weights[a*len(imps) + minIndex] * xMatrix[a][minIndex]
    endTime = time.time()
    return xMatrix.ravel(), endTime - startTime, max(difList) if difList else 0