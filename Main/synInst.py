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


def createAdvsAndImps(numAdvs, numImps, numTypes = 10):
    advsList = []
    for i in range(numAdvs):
        advsList.append(Advertiser(numTypes))
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))
    return advsList, impsList


def createSyntheticInstance(numAdvs, numImps, seed = None, numTypes = 10):
    if seed is not None:
        random.seed(seed)

    advsList, impsList = createAdvsAndImps(numAdvs, numImps)

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


# def createSyntheticInstance(numAdvs, numImps, seed = None, corruptNum = 0):
#     # Seed
#     if seed is not None:
#         random.seed(seed)
#     # Advertisers
#     numTypes = 10
#     budgets = createBudgets(numAdvs)
#     advsList = []
#     valuations = []
#     for i in range(numAdvs):
#         advValuations = []
#         for x in range(numTypes):
#             advValuations.append(random.expovariate(1))
#         valuations.append(advValuations)
#         advsList.append(Advertiser(budgets[x]))
#     # Impressions
#     impsList = []
#     types = []
#     for i in range(numImps):
#         types.append(random.randint(0, numTypes-1))
#         impsList.append(Impression())
#     # Weights
#     weights = []
#     for a in range(len(advsList)):
#         for i in range(len(impsList)):
#             weights.append(valuations[a][types[i]])

#     return advsList, impsList, weights
