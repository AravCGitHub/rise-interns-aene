import time
import numpy as np

def removeImpressionWithLowestVal(imps): # helper for algorithm
    for imp in imps:
        val = imp.valWithCurrAdv
        if val == np.min(np.array(imp.valWithCurrAdv)):
            imps.remove(imp)
            # if val != 0:
                # print("REMOVED", val)
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

def solve(advs, imps, alpha):
    # B = np.min([adv.budget for adv in advs])
    # e_B = (1+1/B) ** B
    # alpha_B = B * (e_B ** (alpha/B) - 1)
    startTime = time.time()
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
        imp.number = i
        a_exp.impressions.append(imp)
        removeImpressionWithLowestVal(a_exp.impressions)
        a_exp.beta = updateBeta(a_exp, alpha)
        # a_exp.beta = 1
    endTime = time.time()
    # Printing results
    solve = np.zeros((len(advs),len(imps)))
    # objectiveValue = 0
    for a in range(len(advs)):
        tot = 0
        for imp in advs[a].impressions:
            if imp.valWithCurrAdv != 0:
                # objectiveValue += imp.valWithCurrAdv
                tot += 1
                solve[a][imp.number] = 1
        if tot > advs[a].budget:
            raise Exception("ERROR: Budget exceeded at advertiser", a)

    return solve.ravel(), endTime - startTime
