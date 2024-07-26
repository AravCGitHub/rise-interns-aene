import math
import random
import sys
from impression import Impression
from advertiser import Advertiser

def capWeight(weight):
        # max = (math.log(sys.float_info.max) + 1) * 0.25
        max = 1000
        if weight > max:
            return max
        else:
            return weight

def createSyntheticInstance(numAdvs, numImps, seed = None):
    if seed is not None:
        random.seed(seed)
    numTypes = 10
    advsList = []
    for i in range(numAdvs):
        advsList.append(Advertiser(numTypes))
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))

    weights = []
    for a in advsList:
        for i in impsList:
            weights.append(a.valuations[i.type])

    return advsList, impsList, weights

def corruption1(weights):
    for i in range(len(weights)):
        if random.random() < 0.2:
            weights[i] = 0
    return weights

def corruption2(weights):
    for i in range(len(weights)):
        if random.random() < 0.25:
            weights[i] = capWeight(weights[i]*100)
        elif random.random() > 0.74:
            weights[i] = capWeight(weights[i]/100)
    return weights