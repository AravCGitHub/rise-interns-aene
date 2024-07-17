import random
import numpy as np
import graph
import optimal
import alg1
import alg2
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

def createSyntheticInstance(numAdvs, numImps, seed = 0):
    random.seed(seed)
    numTypes = 10
    advsList = []
    for i in range(numAdvs):
        advsList.append(Advertiser(numTypes))
    impsList = []
    for i in range(numImps):
        type = random.randint(0, numTypes-1)
        impsList.append(Impression(type))
    return advsList, impsList

def objectiveValue(solved, weights):
    npSolv = np.array(solved).ravel()
    dot = np.dot(npSolv * -1, weights)
    return dot

def main():
    figure, axis = plt.subplots(1, 2)
    optSolvedArr, alg1solvedArr, alg2solvedArr = [], [], []
    optTimeArr, alg1TimeArr, alg2TimeArr = [], [], []
    optObjArr, alg1ObjArr, alg2ObjArr = [], [], []
    numImpsArr = []
    for count in range(20):
        numImps = random.randint(100,1000)
        numImpsArr.append(numImps)
        a, i = createSyntheticInstance(50,numImps) # fixed 10 advs, rand 1-100 imps
        weights = optimal.createVectorC(a,i)
        # Optimal Algorithm
        # optSolved, optTimeTaken = (optimal.lpSolve(a,i))
        # optObj = objectiveValue(optSolved, weights)
        # optSolvedArr.append(optSolved)
        # optTimeArr.append(optTimeTaken)
        # optObjArr.append(optObj)
        # print("CVXOPT Objective Value:", optObj)
        # print("Time Taken:", optTimeTaken)
        # Algorithm 1
        alg1Solved, alg1TimeTaken = alg1.solve(a,i,1)
        alg1Obj = objectiveValue(alg1Solved, weights)
        alg1solvedArr.append(alg1Solved)
        alg1TimeArr.append(alg1TimeTaken)
        alg1ObjArr.append(alg1Obj)
        print("Alg1 Objective Value:", alg1Obj)
        print("Time Taken:", alg1TimeTaken)
        # Algorithm 2
        alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,0.5,0.9,10) # lam = 0.1, eps = 1, numRounds = 20
        alg2Obj = objectiveValue(alg2Solved, weights)
        alg2solvedArr.append(alg2Solved)
        alg2TimeArr.append(alg2TimeTaken)
        alg2ObjArr.append(alg2Obj)
        print("Alg2 Objective Value:", alg2Obj)
        print("Time Taken:", alg2TimeTaken)
        # Graphing
        objArr = [optObjArr, alg1ObjArr, alg2ObjArr]
        timeArr = [optTimeArr, alg1TimeArr, alg2TimeArr]
        graph.graphObjandTimeVsImps(objArr, timeArr, numImpsArr)

def test():
    a, i = createSyntheticInstance(50,1000, 1)
    weights = optimal.createVectorC(a,i)
    roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], [] 

    # for rounds in range (1,100):
    #     print("Rounds:", rounds)
    #     alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,0.5,0.9,rounds)
    #     alg2Obj = objectiveValue(alg2Solved, weights)
    #     roundsArr.append(rounds)
    #     maxOverflowArr.append(maxOverflow)
    #     timeArr.append(alg2TimeTaken)
    #     objArr.append(alg2Obj)
    # graph.graph(roundsArr, maxOverflowArr, "Rounds", "MaximumBudgetOverflow")
    # graph.graph(roundsArr, timeArr, "Rounds", "TimeTaken")
    # graph.graph(roundsArr, objArr, "Rounds", "ObjectiveValue")

    # roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], [] 

    for eps in frange(0.01,1.0,0.025):
        print("Epsilon:", eps)
        alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,0.5,eps,20)
        alg2Obj = objectiveValue(alg2Solved, weights)
        epsArr.append(eps)
        maxOverflowArr.append(maxOverflow)
        timeArr.append(alg2TimeTaken)
        objArr.append(alg2Obj)
    graph.graph(epsArr, maxOverflowArr, "Epsilon", "MaximumBudgetOverflow")
    graph.graph(epsArr, timeArr, "Epsilon", "TimeTaken")
    graph.graph(epsArr, objArr, "Epsilon", "ObjectiveValue")

    roundsArr, epsArr, lamArr, maxOverflowArr, timeArr, objArr = [], [], [], [], [], []

    for lam in frange(0.05,1.0,0.025):
        print("Lambda:", lam)
        alg2Solved, alg2TimeTaken, maxOverflow = alg2.solve(a,i,weights,lam,0.9,20)
        alg2Obj = objectiveValue(alg2Solved, weights)
        lamArr.append(lam)
        maxOverflowArr.append(maxOverflow)
        timeArr.append(alg2TimeTaken)
        objArr.append(alg2Obj)
    graph.graph(lamArr, maxOverflowArr, "Lambda", "MaximumBudgetOverflow")
    graph.graph(lamArr, timeArr, "Lambda", "TimeTaken")
    graph.graph(lamArr, objArr, "Lambda", "ObjectiveValue")
        
# main()
test()

# make graph for time v. profit for several algorithms by varying synthetic instance size using matplotlib

# make line graphs
# bigger instances for alg1 and 2 - done
# rounds vs maximum budget overflow - done
# same graphs on bad instances
# make obj vs every parameter for alg2 
# make time vs every parameter for alg2

# make heat map for eps vs lam testing - pick 5 synthetic instances of same size and find avg of obj on each
# sort dictionary and implement best fit lines
# look at paper and create corrupted instances and test them

# End Goal: find tuned params for eps/lam and then test on larger and corrupted instances