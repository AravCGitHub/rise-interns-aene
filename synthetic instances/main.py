import random
import numpy as np
import math
import time
import optimal
import alg1
import alg2
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

def main():
    figure, axis = plt.subplots(1, 2)
    for count in range(20):
        numImps = random.randint(1,100)
        a, i = createSyntheticInstance(10,numImps) # fixed 20 advs, rand 1-100 imps
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
        alg2Solved, alg2TimeTaken = alg2.solve(a,i,weights,0.03,0.01,20) # lam = 0.1, eps = 1, numRounds = 20
        alg2Obj = objectiveValue(alg2Solved, weights)
        print("Alg2 Objective Value:", alg2Obj)
        print("Time Taken:", alg2TimeTaken)
        # print(alg2Solved)
        # Graphing Obj vs Imps
        if (count == 1):
            axis[0].plot(numImps, optObj, 'bo', label = "CVXOPT")
            axis[0].plot(numImps, algObj, 'ro', label = "Algorithm 1")
            axis[0].plot(numImps, alg2Obj, 'go', label = "Algorithm 2")
        else:
            axis[0].plot(numImps, optObj, 'bo')
            axis[0].plot(numImps, algObj, 'ro')
            axis[0].plot(numImps, alg2Obj, 'go')
        axis[0].set_xlabel('Number of Impressions')
        axis[0].set_ylabel('Objective Value')
        # Graphing Time vs Imps
        if (count == 1):
            axis[1].plot(numImps, optTimeTaken, 'bo', label = "CVXOPT")
            axis[1].plot(numImps, algTimeTaken, 'ro', label = "Algorithm 1")
            axis[1].plot(numImps, alg2TimeTaken, 'go', label = "Algorithm 2")
        else:
            axis[1].plot(numImps, optTimeTaken, 'bo')
            axis[1].plot(numImps, algTimeTaken, 'ro')
            axis[1].plot(numImps, alg2TimeTaken, 'go')
        axis[1].set_xlabel('Number of Impressions')
        axis[1].set_ylabel('Time Taken')
    axis[0].legend()
    axis[1].legend()
    plt.tight_layout()
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/image.png')

main()
# test()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib

# make line graphs
# bigger instances for alg1 and 2
# rounds vs maximum budget overflow
# same graphs on bad instances
# make obj vs every parameter for alg2
# make time vs every parameter for alg2