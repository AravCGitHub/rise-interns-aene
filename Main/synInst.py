import random

from oldImp import Impression
from oldAdv import Advertiser

def createBudgets(numAdvs):
    budgets = []
    for i in range(numAdvs):
        budgets.append(random.randint(1, 100))
    return budgets

def createSyntheticInstance(numAdvs, numImps, seed = None, corruptNum = 0):
    if seed is not None:
        random.seed(seed)
    numTypes = 10
    advsList = []
    for i in range(numAdvs):
        advsList.append(Advertiser(numTypes, corruptNum))
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))

    weights = []
    for a in advsList:
        for i in impsList:
            weights.append(a.returnValuation()[i.returnType()])

    return advsList, impsList, weights

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