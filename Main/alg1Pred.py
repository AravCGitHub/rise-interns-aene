import random
import time
import numpy as np
import sys
import optimal
from advertiser import Advertiser
from impression import Impression

def updateBeta1(adv, alpha): # Paper's conservative method
    B = adv.budget
    e = (1+1/B) ** B
    left = (e ** (alpha / B) - 1) / (e ** alpha - 1)
    right = 0
    for i in range(len(adv.impressions)):
        right += (adv.impressions[i].weight) * (e ** ((alpha * (B - i)) / B))
    return left * right

def updateBeta2(adv): # Uniform average of weights
    return sum(imp.weight for imp in adv.impressions) / len(adv.impressions)

def updateBeta3(adv): # Lowest weight
    return adv.impressions[0].weight

def predict(predAns, imp):
    return np.argmax(predAns[:,imp.type])

def solve(advs, imps, weights, alpha, betaUpdateType, predAns = None, usePred = False):
    # Initialize variables
    count = 0 # TODO
    dummy = Advertiser(0) # dummy advertiser for impressions that don't get allocated
    betaArr = np.array([0.0]*len(advs))
    weights = np.array(weights).reshape((len(advs), len(imps)))
    objVal = 0
    B = np.min([adv.budget for adv in advs])
    e_B = (1+1/B) ** B
    alpha_B = B * (e_B ** (alpha/B) - 1)
    print("ALPHAB", alpha_B)
    startTime = time.time()
    # Loop through all impressions
    for i in range(len(imps)):
        t = imps[i]
        t.number = i
        # Find best advertiser for impression
        advIndexEXP = np.argmax(weights[:,i] - betaArr)
        advIndexPRD = predict(predAns, t) if usePred else 0
        discGainEXP = weights[advIndexEXP][i] - betaArr[advIndexEXP]
        discGainPRD = weights[advIndexPRD][i] - betaArr[advIndexPRD]
        # Quick test
        # if advIndexPRD == advIndexEXP:
        #     print("SAME")
        # else:
        #     print("DIFF")
        #     count += 1
        # If discGain small, don't allocate
        if discGainEXP <= 0 and discGainPRD <= 0:
            t.weight = 0
            dummy.impressions.add(t)
            continue
        # If prd better, allocate to prd
        elif alpha_B * discGainPRD > discGainEXP:
            if advIndexPRD != advIndexEXP:
                raise Exception("SAME")
            advIndex = advIndexPRD
            t.weight = weights[advIndex][i]
            advs[advIndex].impressions.add(t)
        # Otherwise, allocate to exp
        else:
            advIndex = advIndexEXP
            t.weight = weights[advIndex][i]
            advs[advIndex].impressions.add(t)
        objVal += t.weight
        # Remove lowest value impression if budget exceeded
        if len(advs[advIndex].impressions) > advs[advIndex].budget:
            minImp = advs[advIndex].impressions.pop(0)
            dummy.impressions.add(minImp)
            objVal -= minImp.weight
        # Update beta value for advertiser
        if betaUpdateType == 1:
            betaArr[advIndex] = updateBeta1(advs[advIndex], alpha)
        elif betaUpdateType == 2:
            betaArr[advIndex] = updateBeta2(advs[advIndex])
        elif betaUpdateType == 3:
            betaArr[advIndex] = updateBeta3(advs[advIndex])
    endTime = time.time()
    for a in range(len(advs)):
        if len(advs[a].impressions) > advs[a].budget:
            raise Exception("ERROR: Budget exceeded at advertiser", a)
    # Create xMatrix
    xMatrix = np.zeros((len(advs), len(imps)))
    for a in range(len(advs)):
        for imp in advs[a].impressions:
            xMatrix[a][imp.number] = 1
    # Clear impressions
    for a in advs:
        a.impressions.clear()
    print("COUNT", count)
    # Return results
    return xMatrix.ravel(), endTime - startTime