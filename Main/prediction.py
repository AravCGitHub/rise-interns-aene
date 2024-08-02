import math
import random
import time
import numpy as np
import sys
import optimal
import synInst
from advertiser import Advertiser
from impression import Impression

def createPrediction2(advs, imps, weights):
    optSolved, optTimeTaken = (optimal.lpSolve(advs,imps,weights))
    for x in range(len(optSolved)):
        optSolved[x] = round(optSolved[x])
        if optSolved[x] == 1:
            rand = random.randint(1,100)
            if rand <= 10:
                optSolved[x] = 0
    return optSolved.reshape(len(advs), len(imps))




def createPrediction1(advs, numImps = 100):
    numTypes = len(advs[0].valuations) # make sure this is less than numImps
    imps = []
    for type in range(numTypes):
        imps.append(Impression(type))
    for i in range(numImps - numTypes):
        type = random.randint(0, numTypes-1)
        imps.append(Impression(type))
    weights = synInst.createWeights(advs, imps)
    optSolved, optTimeTaken = (optimal.lpSolve(advs,imps,weights))
    predAns = np.zeros((len(advs), numTypes))
    for a in range(len(optSolved)):
        if round(optSolved[a]) == 1:
            advIndex = a // numImps
            impIndex = a % numImps
            predAns[advIndex][imps[impIndex].type] += 1
    return predAns