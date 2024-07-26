import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import advertiser
import impression
import data
import graph
import synInst
import tuning
import alg1
import alg2
import optimal


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
        a, i, w = synInst.createSyntheticInstance(50, count, corruptNum=0)
        # numA, numI, w = bigData()
        # a, i, _ = createSyntheticInstance(numA, numI, corruptNum=3)
        # Optimal Algorithm
        # if count <= -1:
            # optSolved, optTimeTaken = (optimal.lpSolve(a,i,w))
            # optObj = objectiveValue(optSolved, w)
            # optSolvedArr.append(optSolved)
            # optTimeArr.append(optTimeTaken)
            # optObjArr.append(optObj)
            # print("CVXOPT Objective Value:", optObj)
            # print("Time Taken:", optTimeTaken)
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

main()