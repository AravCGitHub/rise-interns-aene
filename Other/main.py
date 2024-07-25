import random
import time
import numpy as np
import graph
import optimal
import alg1
import alg2
import oldAlg2
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression
import seaborn as sns
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

    return advsList, impsList, weights

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
    numImpsArr = []
    count = 0
    for loop in range(50):
        print(loop)
        count += 20
        a, i, w = createSyntheticInstance(50, count, corruptNum=0)
        # numA, numI, w = bigData()
        # a, i, _ = createSyntheticInstance(numA, numI, corruptNum=3)
        # Optimal Algorithm
        # if count <= -1:
        #     optSolved, optTimeTaken = (optimal.lpSolve(a,i,w))
        #     optObj = objectiveValue(optSolved, w)
        #     optSolvedArr.append(optSolved)
        #     optTimeArr.append(optTimeTaken)
        #     optObjArr.append(optObj)
        #     print("CVXOPT Objective Value:", optObj)
        #     print("Time Taken:", optTimeTaken)
        # else:
        #     optTimeArr.append(0)
        #     optObjArr.append(0)
        optSolved, optTimeTaken = alg1.solve(a,i,w,1,1)
        optObj = objectiveValue(optSolved, w)
        optSolvedArr.append(optSolved)
        optTimeArr.append(optTimeTaken)
        optObjArr.append(optObj)
        print("CVXOPT Objective Value:", optObj)
        print("Time Taken:", optTimeTaken)
        # Algorithm 1
        alg1Solved, alg1TimeTaken = alg1.solve(a,i,w,1,2)
        alg1Obj = objectiveValue(alg1Solved, w)
        alg1solvedArr.append(alg1Solved)
        alg1TimeArr.append(alg1TimeTaken)
        alg1ObjArr.append(alg1Obj)
        print("Alg1 Objective Value:", alg1Obj)
        print("Time Taken:", alg1TimeTaken)
        # Algorithm 2
        alg2Solved, alg2TimeTaken = alg1.solve(a,i,w,1,3) # lam = 0.25, eps = 0.21, numRounds = 50
        alg2Obj = objectiveValue(alg2Solved, w)
        alg2solvedArr.append(alg2Solved)
        alg2TimeArr.append(alg2TimeTaken)
        alg2ObjArr.append(alg2Obj)
        print("Alg2 Objective Value:", alg2Obj)
        print("Time Taken:", alg2TimeTaken)
        # Graphing
        objArr = [optObjArr[loop], alg1ObjArr[loop], alg2ObjArr[loop]]
        timeArr = [optTimeArr[loop],alg1TimeArr[loop], alg2TimeArr[loop]]
        impsObjVal[count] = objArr
        impsTime[count] = timeArr
    numImpsArr = list(impsObjVal.keys())
    numImpsArr.sort()
    sortedImpsObjVal = [impsObjVal[i] for i in numImpsArr]
    sortedImpsTime = [impsTime[i] for i in numImpsArr]
    graph.graphObjandTimeVsImps(sortedImpsObjVal, sortedImpsTime, numImpsArr)

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

def bigData():
    dataset = data.read_data()
    df, advNum, maxImpId = data.dataToDF(dataset, 4)
    weights, impNum = data.createWeightMatrix(df, advNum, maxImpId)
    print(impNum)
    return advNum, impNum, weights

main()
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