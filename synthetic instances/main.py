import random
import time
import numpy as np
import graph
import optimal
import alg1
import alg2
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression
import seaborn as sns
import brokenAlg1
import data

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

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

    budgets = []
    for a in advsList:
        budgets.append(a.budget)

    return advsList, impsList, weights, budgets


def objectiveValue(solved, weights):
    npSolv = np.array(solved).ravel()
    dot = np.dot(npSolv, weights)
    return dot



def main():
    figure, axis = plt.subplots(1, 2)
    impsObjVal, impsTime = {}, {}
    optSolvedArr, alg1solvedArr, alg2solvedArr = [], [], []
    optTimeArr, alg1TimeArr, alg2TimeArr = [], [], []
    optObjArr, alg1ObjArr, alg2ObjArr = [], [], []
    Oalg1solvedArr, Oalg1TimeArr, Oalg1ObjArr = [], [], []
    numImpsArr = []
    count = 0
    for loop in range(10):
        print(loop)
        count += 10
        a, i, w, b = createSyntheticInstance(30, count) # fixed 10 advs, rand 1-100 imps
        # Optimal Algorithm
        if count <= 100:
            optSolved, optTimeTaken = (optimal.lpSolve(a,i, w))
            print(optSolved)
            optObj = objectiveValue(optSolved, w)
            optSolvedArr.append(optSolved)
            optTimeArr.append(optTimeTaken)
            optObjArr.append(optObj)
            print("CVXOPT Objective Value:", optObj)
            print("Time Taken:", optTimeTaken)
        else:
            optTimeArr.append(0)
            optObjArr.append(0)
        # Algorithm 1
        alg1Solved, alg1TimeTaken = alg1.solve(a,i,w,b,1)
        alg1Obj = objectiveValue(alg1Solved, w)
        alg1solvedArr.append(alg1Solved)
        alg1TimeArr.append(alg1TimeTaken)
        alg1ObjArr.append(alg1Obj)
        print("Alg1 Objective Value:", alg1Obj)
        # print("Time Taken:", alg1TimeTaken)
        # Old Algorithm 1
        Oalg1Solved, Oalg1TimeTaken = oldAlg1.solve(a,i,1)
        Oalg1Obj = objectiveValue(Oalg1Solved, w)
        Oalg1solvedArr.append(Oalg1Solved)
        Oalg1TimeArr.append(Oalg1TimeTaken)
        Oalg1ObjArr.append(Oalg1Obj)
        print("OldAlg1 Objective Value:", Oalg1Obj)




        # Algorithm 2
        # alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,w,0.25,0.21,50) # lam = 0.25, eps = 0.21, numRounds = 50
        # alg2Obj = objectiveValue(alg2Solved, w)
        # alg2solvedArr.append(alg2Solved)
        # alg2TimeArr.append(alg2TimeTaken)
        # alg2ObjArr.append(alg2Obj)
        # print("Alg2 Objective Value:", alg2Obj)
        # print("Time Taken:", alg2TimeTaken)
        # Graphing
        objArr = [optObjArr[loop], alg1ObjArr[loop], Oalg1ObjArr[loop]]
        timeArr = [optTimeArr[loop],alg1TimeArr[loop], Oalg1TimeArr[loop]]
        impsObjVal[count] = objArr
        impsTime[count] = timeArr
    numImpsArr = list(impsObjVal.keys())
    numImpsArr.sort()
    sortedImpsObjVal = [impsObjVal[i] for i in numImpsArr]
    sortedImpsTime = [impsTime[i] for i in numImpsArr]
    graph.graphObjandTimeVsImps(sortedImpsObjVal, sortedImpsTime, numImpsArr)

def test():
    a, i = createSyntheticInstance(50,1000, 1)
    weights = optimal.createVectorC(a,i)
    roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], [] 

    for rounds in range (1,100):
        print("Rounds:", rounds)
        alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,0.25,0.21,rounds)
        alg2Obj = objectiveValue(alg2Solved, weights)
        roundsArr.append(rounds)
        maxOverflowArr.append(maxOverflow)
        timeArr.append(alg2TimeTaken)
        objArr.append(alg2Obj)
    graph.graph(roundsArr, maxOverflowArr, "Rounds", "MaximumBudgetOverflow")
    graph.graph(roundsArr, timeArr, "Rounds", "TimeTaken")
    graph.graph(roundsArr, objArr, "Rounds", "ObjectiveValue")

    # roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], [] 

    # for eps in frange(0.01,1.0,0.025):
    #     print("Epsilon:", eps)
    #     alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,0.5,eps,20)
    #     alg2Obj = objectiveValue(alg2Solved, weights)
    #     epsArr.append(eps)
    #     maxOverflowArr.append(maxOverflow)
    #     timeArr.append(alg2TimeTaken)
    #     objArr.append(alg2Obj)
    # graph.graph(epsArr, maxOverflowArr, "Epsilon", "MaximumBudgetOverflow")
    # graph.graph(epsArr, timeArr, "Epsilon", "TimeTaken")
    # graph.graph(epsArr, objArr, "Epsilon", "ObjectiveValue")

    # roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], []

    # for lam in frange(0.05,1.0,0.025):
    #     print("Lambda:", lam)
    #     alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,lam,0.9,20)
    #     alg2Obj = objectiveValue(alg2Solved, weights)
    #     lamArr.append(lam)
    #     maxOverflowArr.append(maxOverflow)
    #     timeArr.append(alg2TimeTaken)
    #     objArr.append(alg2Obj)
    # graph.graph(lamArr, maxOverflowArr, "Lambda", "MaximumBudgetOverflow")
    # graph.graph(lamArr, timeArr, "Lambda", "TimeTaken")
    # graph.graph(lamArr, objArr, "Lambda", "ObjectiveValue")

def tuneEpsLam():
    aArr, iArr, weightsArr = [], [], []
    for c in range(5):
        a, i = createSyntheticInstance(50,1000, c)
        aArr.append(a)
        iArr.append(i)
        weightsArr.append(optimal.createVectorC(a,i))
    eps_lam_dict1 = {}
    eps_lam_dict2 = {}
    for eps in frange(0.01, 1.0, 0.5):
        for lam in frange(0.05, 1, 0.5):
            print("Epsilon:", eps, "Lambda:", lam)
            objArr = []
            for (a, i, weights) in zip(aArr, iArr, weightsArr):
                alg2Solved, _, _ = alg2.solve(a,i,weights,lam,eps,50)
                alg2Obj = objectiveValue(alg2Solved, weights)
                objArr.append(alg2Obj)
            avgObj = sum(objArr) / len(objArr)
            stdDev = np.std(objArr)
            alg2Obj = avgObj
            eps_lam_dict1[(round(eps,3), round(lam,3))] = alg2Obj
            eps_lam_dict2[(round(eps,3), round(lam,3))] = stdDev
    eps_values1 = sorted(set(eps for eps, _ in eps_lam_dict1.keys()))
    lam_values1 = sorted(set(lam for _, lam in eps_lam_dict1.keys()))
    obj_values = [[eps_lam_dict1[(eps, lam)] for eps in eps_values1] for lam in lam_values1]
    sns.heatmap(obj_values, cmap = "rocket", xticklabels=eps_values1, yticklabels=lam_values1)
    plt.xlabel('Epsilon')
    plt.ylabel('Lambda')
    plt.title('Objective Value Heatmap')
    plt.show()

def testSnap():
    dataset = data.read_data()
    df, advNum, impNum = data.dataToDF(dataset, advNum=100)
    weights = data.createWeightMatrix(df, advNum, impNum)


testSnap()
# main()
# test()
# tuneEpsLam() # lam = 0.25, eps = 0.435
# t3()
    

# make heat map for eps vs lam testing - pick 5 synthetic instances of same size and find avg of obj on each
# sort dictionary and implement best fit lines
# look at paper and create corrupted instances and test them

# End Goal: find tuned params for eps/lam and then test on larger and corrupted instances

# New parameter tuning for eps and lam using more rounds and less jumps

# use big datasets
# transition to latex
# difference plot
# run cvxopt vs algs on smaller instances (cor and not)