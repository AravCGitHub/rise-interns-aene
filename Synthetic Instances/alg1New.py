import time
import numpy as np
import sys

def updateBeta(alpha, index, weights, budget, numImps): # helper for algorithm
   # Calculate left fraction
   e_B_a = (1+1/budget) ** budget
   left = (e_B_a ** (alpha / budget) - 1) / (e_B_a ** alpha - 1)
   # Calculate right summation
   valuationArr = np.array([weights[i] for i in range(numImps*index, numImps*index+numImps)])
   constArr = np.array([e_B_a ** ((alpha * (budget - 1)) / budget)] * len(valuationArr))
   right = np.dot(valuationArr, constArr)
   # Return product of left and right
   return left * right


def solve(advs, imps, weights, budgets, alpha):
   weights = [-w for w in weights]
   startTime = time.time()
   xMatrix = np.array([0]*len(advs)*len(imps))
   betaArr = np.array([0]*len(advs))
   for i in range(len(imps)):
       npWMT = [] # weight minus threshold list
       for a in range(len(advs)):
           val = weights[a*len(imps) + i]
           beta = betaArr[a]
           npWMT.append(val - beta)
       index = np.argmax(npWMT)
       # imp.valWithCurrAdv = weights[index*len(imps) + i]
       # a_exp.impressions.append(imp)
       xMatrix[index*len(imps)+i] = 1
       advWeights = weights[index*len(imps):index*len(imps)+len(imps)]
       miniXMatrix = xMatrix[index*len(imps):index*len(imps)+len(imps)]
       allocatedImps = np.sum(miniXMatrix)


       print("impNum:", i, " advNum", index)
       print("mini xMatrix", xMatrix[index*len(imps):index*len(imps)+len(imps)])
       print("full xMatrix", xMatrix)
       print("allocatedNum", allocatedImps, " BudgetNum", budgets[index], "\n")


       if allocatedImps > budgets[index]:
           min = sys.float_info.max
           minIndex = 0
           for x in range(len(miniXMatrix)):
               if miniXMatrix[x] != 0 and advWeights[x] < min:
                   min = advWeights[x]
                   minIndex = x
           minIndex += index*len(imps)
           xMatrix[minIndex] = 0
           print(minIndex)


       betaArr[index] = updateBeta(alpha, index, weights, budgets[index], len(imps))
   endTime = time.time()
   return xMatrix.ravel(), endTime - startTime