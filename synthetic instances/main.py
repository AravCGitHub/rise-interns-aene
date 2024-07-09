import random
import numpy as np
import time
import optimal
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

def removeImpressionWithLowestVal(imps): # helper for algorithm
    for imp in imps:
        val = imp.valWithCurrAdv
        if val == np.min(np.array(imp.valWithCurrAdv)):
            imps.remove(imp)
            break

def updateBeta(a_exp, alpha): # helper for algorithm
    # Calculate left fraction
    e_B_a = (1+1/a_exp.budget) ** a_exp.budget
    left = (e_B_a ** (alpha / a_exp.budget) - 1) / (e_B_a ** alpha - 1)
    # Calculate right summation
    valuationArr = np.array([imp.valWithCurrAdv for imp in a_exp.impressions])
    constArr = np.array([e_B_a ** ((alpha * (a_exp.budget - 1)) / a_exp.budget)] * len(valuationArr))
    right = np.dot(valuationArr, constArr)
    # Return product of left and right
    return left * right

def algorithm(advs, imps, alpha):
    B = np.min([adv.budget for adv in advs])
    e_B = (1+1/B) ** B
    alpha_B = B * (e_B ** (alpha/B) - 1) # e_B and alpha_B are never used?
    for i in range(len(imps)):
        imp = imps[i] # in case we need to track imp #
        type = imp.returnType()
        npWMT = [] # weight minus threshold list
        for adv in advs:
            val = adv.valuations[type]
            beta = adv.returnBeta()
            npWMT.append(val - beta)
        a_exp = advs[np.argmax(npWMT)] # find advertiser with highest weight minus threshold
        imp.valWithCurrAdv = a_exp.returnValuation()[type]
        a_exp.impressions.append(imp)
        removeImpressionWithLowestVal(a_exp.impressions)
        a_exp.beta = updateBeta(a_exp, alpha)
    # Printing results
    objectiveValue = 0
    print("Advertiser - Impression - Value")
    for adv in advs:
        for imp in adv.impressions:
            if imp.valWithCurrAdv != 0:
                print(adv, "-", imp, "-", imp.valWithCurrAdv)
                objectiveValue += imp.valWithCurrAdv
    print("--------------------")
    print("Objective Value: ", objectiveValue)
    print("--------------------")

def main():
    for count in range(1):
        a, i = createSyntheticInstance(3,50)
        solved, timeTaken = (optimal.lpSolve(a,i))
        print(timeTaken)
        objVal = objectiveValue(solved, optimal.createVectorC(a,i))
        print("CVXOPT Objective Value:", objVal)
        # plt.plot(timeTaken, objVal, 'ro')
        # plt.xlabel('Time Taken')
        # plt.ylabel('Objective Value')
        algorithm(a,i,1)
    # plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/TimeVProfit.png')

main()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib
# objective value v impressions, time v impressions, comparing cvxopt and algo
# obj value vs size

# e_B and A_B questions
# do we have to allocate B_a zero value impressions and remove lowest as we go through or is there a better way