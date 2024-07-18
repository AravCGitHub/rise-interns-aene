import random
import numpy as np
from sklearn.metrics import r2_score
import math
import time
import optimal
import alg1
import alg2
import matplotlib.pyplot as plt
from advertiser import Advertiser
from impression import Impression

def graphObjandTimeVsImps(objArr, timeArr, numImps):
    figure, axis = plt.subplots(1, 2)
    objArrCVX, objArrAlg1, objArrAlg2, timeArrCVX, timeArrAlg1, timeArrAlg2 = [], [], [], [], [], []
    
    # Make models
    for i in range(len(objArr)):
        #change indexing when using CVXOPT
        # objArrCVX.append(objArr[i][0])
        objArrAlg1.append(objArr[i][0])
        objArrAlg2.append(objArr[i][1])
        # timeArrCVX.append(timeArr[i][0])
        timeArrAlg1.append(timeArr[i][0])
        timeArrAlg2.append(timeArr[i][1])
 
    # objModelCVX = np.poly1d(np.polyfit(numImps, objArrCVX, 3))
    objModelAlg1= np.poly1d(np.polyfit(numImps, objArrAlg1, 3))
    objModelAlg2 = np.poly1d(np.polyfit(numImps, objArrAlg2, 3))

    # timeModelCVX = np.poly1d(np.polyfit(numImps, timeArrCVX, 2))
    timeModelAlg1 = np.poly1d(np.polyfit(numImps, timeArrAlg1, 2))
    timeModelAlg2 = np.poly1d(np.polyfit(numImps, timeArrAlg2, 2))

    # Plot Data
    # axis[0].scatter(numImps, objArrCVX, c='red', label='CVXOPT')
    axis[0].scatter(numImps, objArrAlg1, c='green', label='Algorithm 1')
    axis[0].scatter(numImps, objArrAlg2, c='blue', label='Algorithm 2')
    # axis[1].scatter(numImps, timeArrCVX, c='red', label='CVXOPT')
    axis[1].scatter(numImps, timeArrAlg1, c='green', label='Alg 1')
    axis[1].scatter(numImps, timeArrAlg2, c='blue',label='Alg 2')

    # axis[0].plot(numImps, objModelCVX(numImps), color='red')
    axis[0].plot(numImps, objModelAlg1(numImps), color='green')
    axis[0].plot(numImps, objModelAlg2(numImps), color='blue')
    # axis[1].plot(numImps, timeModelCVX(numImps), color='red')
    axis[1].plot(numImps, timeModelAlg1(numImps), color='green')
    axis[1].plot(numImps, timeModelAlg2(numImps), color='blue')

    # Labels
    axis[0].set_xlabel('Number of Impressions')
    axis[0].set_ylabel('Objective Value')
    axis[1].set_xlabel('Number of Impressions')
    axis[1].set_ylabel('Time Taken')
    axis[0].legend()
    axis[1].legend()
    plt.tight_layout()
    # Save and Clear

    plt.savefig('/Users/forev/rise-interns-aene/Images/ObjTimeVsImps.png')
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
    plt.savefig('/Users/forev/rise-interns-aene/Images/' + xlabel + 'Vs' + ylabel + '.png')
    plt.cla()
    plt.clf()
    plt.close()
