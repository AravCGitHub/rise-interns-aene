import random
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression

def graphObjandTimeVsImps(objArr, timeArr, numImpsArr):
    figure, axis = plt.subplots(1, 2)
    objArrCVX, objArrAlg1, objArrAlg2, timeArrCVX, timeArrAlg1, timeArrAlg2 = [], [], [], [], [], []
    
    # Make models
    for i in range(len(objArr)):
        #change indexing when ignoring CVXOPT
        objArrCVX.append(objArr[i][0])
        objArrAlg1.append(objArr[i][1])
        objArrAlg2.append(objArr[i][2])
        timeArrCVX.append(timeArr[i][0])
        timeArrAlg1.append(timeArr[i][1])
        timeArrAlg2.append(timeArr[i][2])

    axis[0].plot(numImpsArr, objArrCVX, c='red', label="CVXOPT")
    axis[0].plot(numImpsArr, objArrAlg1, c='green', label='Algorithm 1')
    axis[0].plot(numImpsArr, objArrAlg2, c='blue', label='Algorithm 2')
    axis[1].plot(numImpsArr, timeArrCVX, c='red', label='CVXOPT')
    axis[1].plot(numImpsArr, timeArrAlg1, c='green', label='Algorithm 1')
    axis[1].plot(numImpsArr, timeArrAlg2, c='blue', label='Algorithm 2')

    # axis[0].plot(numImpsArr, objArrCVX, c='red', label="Paper Method")
    # axis[0].plot(numImpsArr, objArrAlg1, c='green', label='Uniform Average')
    # axis[0].plot(numImpsArr, objArrAlg2, c='blue', label='Lowest Weight')
    # axis[1].plot(numImpsArr, timeArrCVX, c='red', label='Paper Method')
    # axis[1].plot(numImpsArr, timeArrAlg1, c='green', label='Uniform Average')
    # axis[1].plot(numImpsArr, timeArrAlg2, c='blue', label='Lowest Weight')

    # Labels
    axis[0].set_xlabel('Number of Impressions')
    axis[0].set_ylabel('Objective Value')
    axis[1].set_xlabel('Number of Impressions')
    axis[1].set_ylabel('Time Taken')
    axis[0].legend()
    axis[1].legend()
    plt.tight_layout()
    # Save and Clear
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/New.png')
    plt.cla()
    plt.clf()
    plt.close()

def graphDifference(objArr, timeArr, numImpsArr):
    figure, axis = plt.subplots(1, 2)
    objValDif, timeDif = [], []
    # Make models
    for i in range(len(objArr)):
        objValDif.append(objArr[i][1] - objArr[i][0]) #will be the second alg passed minus the first
        timeDif.append(timeArr[i][1] - timeArr[i][0])

    axis[0].plot(numImpsArr, objValDif, color='blue', label='CVXOpt - Alg1')
    axis[1].plot(numImpsArr, timeDif, color='blue', label='CVXOpt - Alg1')

    axis[0].set_xlabel('Number of Impressions')
    axis[0].set_ylabel('Difference in Objective Value')
    axis[1].set_xlabel('Number of Impressions')
    axis[1].set_ylabel('Difference in Time Taken')
    axis[0].legend()
    axis[1].legend()
    plt.tight_layout()
    # Save and Clear

    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/ObjTimeVsImpsDif.png')
    plt.cla()
    plt.clf()
    plt.close()

def graph(x, y, xlabel, ylabel):
    #do r2 stuff
    bestModel = np.poly1d(np.polyfit(x, y, 1))
    max_r2 = r2_score(y, bestModel(x))

    for n in range(2, 20):
        model = np.poly1d(np.polyfit(x, y, n))
        r2 = r2_score(y, model(x))
        if r2 > max_r2:
            max_r2 = r2
            bestModel = model

    plt.scatter(x, y, color='blue')
    plt.plot(x, bestModel(x), color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/' + xlabel + 'Vs' + ylabel + '.png')
    plt.cla()
    plt.clf()
    plt.close()