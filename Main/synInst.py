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

def createImps(numImps, seed = None, numTypes = 10):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))
    return impsList

def createAdvs(numAdvs, numImps, seed = None, numTypes = 10):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    advsList = []
    impsPerAdv = round((numImps / numAdvs) * 0.75)
    ran = round(impsPerAdv * 2 / 3)
    for i in range(numAdvs):
        if max(impsPerAdv-ran,1) != impsPerAdv+ran:
            budget = random.randint(max(impsPerAdv-ran,1), impsPerAdv+ran)
        else:
            budget = impsPerAdv+ran
        advsList.append(Advertiser(numTypes, budget))
    return advsList

def createWeights(advsList, impsList):
    weights = []
    for a in advsList:
        for i in impsList:
            weights.append(a.valuations[i.type])
    return weights

def createSyntheticInstance(numAdvs, numImps, advsSeed = None, impsSeed = None, numTypes = 10):
    advsList = createAdvs(numAdvs, numImps, advsSeed, numTypes)
    impsList = createImps(numImps, impsSeed, numTypes)
    weights = createWeights(advsList, impsList)
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