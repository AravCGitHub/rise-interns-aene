import random
import numpy as np
import math
import time
import optimal
import alg1
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

def objectiveValue(solved, weights):
    npSolv = np.array(solved).ravel()
    dot = np.dot(npSolv * -1, weights)
    return dot

def calculateD(adv, imp, lam):
    val = adv.valuations[imp.type]
    D = math.e ** (val / lam - 1)
    return D

def alg2(advs, imps, lam, eps, numRounds):
    xMatrix = np.zeros((len(advs), len(imps)))
    priorityScores = [(1+eps) ** -numRounds] * len(advs)
    for r in range(numRounds):
        # Step 1
        for i in range (len(imps)):
            sum = 0
            for a in range (len(advs)):
                D_a = calculateD(advs[a], imps[i], lam)
                sum += priorityScores[a] * D_a
            for a in range (len(advs)):
                if (sum <= 1):
                    xMatrix[a][i] = priorityScores[a] * calculateD(advs[a], imps[i], lam)
                else:
                    xMatrix[a][i] = (priorityScores[a] * calculateD(advs[a], imps[i], lam)) / sum
        # Step 2
        for a in range (len(advs)):
            alloc = xMatrix[a].sum()
            if (alloc <= (advs[a].budget) / (1 + eps)):
                priorityScores[a] = (1 + eps) * priorityScores[a]
            if (alloc >= (advs[a].budget) * (1 + eps)):
                priorityScores[a] = priorityScores[a] / (1 + eps)
    # Final Check
    for a in range (len(advs)):
        if (xMatrix[a].sum() > advs[a].budget):
            N_a = 0
            for val in xMatrix[a]:
                if (val > 0):
                    N_a += 1
            reductionFactor = advs[a].budget / N_a
            for i in range (len(imps)):
                xMatrix[a][i] = xMatrix[a][i] * reductionFactor
                if (xMatrix[a].sum() <= advs[a].budget):
                    break
    return xMatrix
        
def test():
    advs, imps = createSyntheticInstance(3, 5)
    lam = 1
    eps = 0.1
    numRounds = 10
    alg2Solved = alg2(advs, imps, lam, eps, numRounds)
    weights = optimal.createVectorC(advs, imps)
    obj = objectiveValue(alg2Solved, weights)
    print (alg2Solved)
    print("Objective Value:", obj)


def main():
    figure, axis = plt.subplots(1, 2)
    for count in range(1):
        numImps = random.randint(1,100)
        a, i = createSyntheticInstance(10,100) # fixed 20 advs, rand 1-100 imps
        weights = optimal.createVectorC(a,i)
        # Optimal Algorithm
        optSolved, optTimeTaken = (optimal.lpSolve(a,i))
        optObj = objectiveValue(optSolved, weights)
        print("CVXOPT Objective Value:", optObj)
        print("Time Taken:", optTimeTaken)
        # print(optSolved)
        # Algorithm 1
        algSolved, algTimeTaken = alg1.solve(a,i,1)
        algObj = objectiveValue(algSolved, weights)
        print("Alg1 Objective Value:", algObj)
        print("Time Taken:", algTimeTaken)
        # print(algSolved)
        # Algorithm 2
        alg2Solved = alg2(a,i,0.1,0.01,20) # lam = 0.1, eps = 1, numRounds = 20
        alg2Obj = objectiveValue(alg2Solved, weights)
        print("Alg2 Objective Value:", alg2Obj)
        # print(alg2Solved)
    #     # Graphing Obj vs Imps
    #     if (count == 1):
    #         axis[0].plot(numImps, optObj, 'bo', label = "CVXOPT")
    #         axis[0].plot(numImps, algObj, 'ro', label = "Algorithm 1")
    #     else:
    #         axis[0].plot(numImps, optObj, 'bo')
    #         axis[0].plot(numImps, algObj, 'ro')
    #     axis[0].set_xlabel('Number of Impressions')
    #     axis[0].set_ylabel('Objective Value')
    #     # Graphing Time vs Imps
    #     if (count == 1):
    #         axis[1].plot(numImps, optTimeTaken, 'bo', label = "CVXOPT")
    #         axis[1].plot(numImps, algTimeTaken, 'ro', label = "Algorithm 1")
    #     else:
    #         axis[1].plot(numImps, optTimeTaken, 'bo')
    #         axis[1].plot(numImps, algTimeTaken, 'ro')
    #     axis[1].set_xlabel('Number of Impressions')
    #     axis[1].set_ylabel('Time Taken')
    # axis[0].legend()
    # axis[1].legend()
    # plt.tight_layout()
    # plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/image.png')

main()
# test()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib