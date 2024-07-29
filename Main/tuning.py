import synInst
import alg2
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

def objectiveValue(solved, weights):
    npSolv = np.array(solved).ravel()
    dot = np.dot(npSolv, weights)
    return dot

def tuneEpsLam():
    aArr, iArr, weightsArr = [], [], []
    for c in range(5):
        a, i, w = synInst.createSyntheticInstance(50,1000, c)
        aArr.append(a)
        iArr.append(i)
        weightsArr.append(w)
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