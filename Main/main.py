import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import advertiser
import impression
# import data
import graph
import synInst
import alg1
import alg1Pred
import alg2
import optimal
from prediction import createPredictions
from tuning import objectiveValue

def main():
    figure, axis = plt.subplots(1, 2)
    impsObjVal, impsTime = {}, {}
    optSolvedArr, alg1solvedArr, alg2solvedArr = [], [], []
    optTimeArr, alg1TimeArr, alg2TimeArr = [], [], []
    optObjArr, alg1ObjArr, alg2ObjArr = [], [], []
    numImpsArr = []
    count = 0
    aP = synInst.createAdvs(10,0) # numAdvs, advsSeed
    predAns = createPredictions(aP, 100)
    print(predAns)
    for loop in range(2):
        print(loop)
        count += 20
        a, i, w = synInst.createSyntheticInstance(10, 10000, advsSeed=0) # numAdvs, numImps, seed, advsSeed, numTypes
        # numA, numI, w = bigData()
        # Optimal Algorithm
        if count <= -1:
            optSolved, optTimeTaken = (optimal.lpSolve(a,i,w))
            optObj = objectiveValue(optSolved, w)
            optSolvedArr.append(optSolved)
            optTimeArr.append(optTimeTaken)
            optObjArr.append(optObj)
            print("CVXOPT Objective Value:", optObj)
            print("Time Taken:", optTimeTaken)
        else:
            optTimeArr.append(0)
            optObjArr.append(0)
        # optSolved, optTimeTaken = alg1.solve(a,i,w,1,1)
        # optObj = objectiveValue(optSolved, w)
        # optSolvedArr.append(optSolved)
        # optTimeArr.append(optTimeTaken)
        # optObjArr.append(optObj)
        # print("CVXOPT Objective Value:", optObj)
        # print("Time Taken:", optTimeTaken)
        # Algorithm 1
        alg1Solved, alg1TimeTaken = alg1Pred.solve(a,i,w,1,1,predAns,True)
        alg1Obj = objectiveValue(alg1Solved, w)
        alg1solvedArr.append(alg1Solved)
        alg1TimeArr.append(alg1TimeTaken)
        alg1ObjArr.append(alg1Obj)
        print("Alg1 Objective Value:", alg1Obj)
        print("Time Taken:", alg1TimeTaken)
        # Algorithm 2
        # alg2Solved, alg2TimeTaken, _ = alg2.solve(a,i,w,0.25,0.21,50) # lam = 0.25, eps = 0.21, numRounds = 50
        alg2Solved, alg2TimeTaken = alg1.solve(a,i,w,1,1)
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