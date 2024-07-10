import random
import numpy as np
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

def main():
    for count in range(20):
        numImps = random.randint(1,100)
        a, i = createSyntheticInstance(10,numImps) # fixed 10 advs, rand 1-50 imps
        weights = optimal.createVectorC(a,i)
        # Optimal Algorithm
        optSolved, optTimeTaken = (optimal.lpSolve(a,i))
        optObj = objectiveValue(optSolved, weights)
        print("CVXOPT Objective Value:", optObj)
        print("Time Taken:", optTimeTaken)
        # Algorithm 1
        algSolved, algTimeTaken = alg1.solve(a,i,1)
        algObj = objectiveValue(algSolved, weights)
        print("Alg1 Objective Value:", algObj)
        print("Time Taken:", algTimeTaken)

        # Graphing Obj vs Imps
        if (count == 1):
            plt.plot(numImps, optObj, 'bo', label = "CVXOPT")
            plt.plot(numImps, algObj, 'ro', label = "Algorithm 1")
            plt.legend()
        else:
            plt.plot(numImps, optObj, 'bo')
            plt.plot(numImps, algObj, 'ro')
        plt.xlabel('Number of Impressions')
        plt.ylabel('Objective Value')
        # Graphing Time vs Imps
        # if (count == 1):
        #     plt.plot(numImps, optTimeTaken, 'bo', label = "CVXOPT")
        #     plt.plot(numImps, algTimeTaken, 'ro', label = "Algorithm 1")
        #     plt.legend()    
        # else:
        #     plt.plot(numImps, optTimeTaken, 'bo')
        #     plt.plot(numImps, algTimeTaken, 'ro')
        # plt.xlabel('Number of Impressions')
        # plt.ylabel('Time Taken')
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/TimeVProfit.png')

main()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib
# objective value v impressions, time v impressions, comparing cvxopt and algo
# obj value vs size

# figure, axis = plt.subplots(2)
#         # Graphing Obj vs Imps
#         if (count == 1):
#             axis[0].plot(numImps, optObj, 'bo', label = "CVXOPT")
#             axis[0].plot(numImps, algObj, 'ro', label = "Algorithm 1")
#         else:
#             axis[0].plot(numImps, optObj, 'bo')
#             axis[0].plot(numImps, algObj, 'ro')
#         axis[0].set_xlabel('Number of Impressions')
#         axis[0].set_ylabel('Objective Value')
#         # Graphing Time vs Imps
#         if (count == 1):
#             axis[1].plot(numImps, optTimeTaken, 'bo', label = "CVXOPT")
#             axis[1].plot(numImps, algTimeTaken, 'ro', label = "Algorithm 1")
#         else:
#             axis[1].plot(numImps, optTimeTaken, 'bo')
#             axis[1].plot(numImps, algTimeTaken, 'ro')
#         axis[1].set_xlabel('Number of Impressions')
#         axis[1].set_ylabel('Time Taken')
#     axis[0].legend()
#     axis[1].legend()