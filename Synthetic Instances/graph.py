import random
import numpy as np
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
    # Plot Data
    # axis[0].plot(numImps, objArr[0], 'bo', label = "CVXOPT")
    axis[0].plot(numImps, objArr[1], 'ro', label = "Algorithm 1")
    axis[0].plot(numImps, objArr[2], 'go', label = "Algorithm 2")
    # axis[1].plot(numImps, timeArr[0], 'bo', label = "CVXOPT")
    axis[1].plot(numImps, timeArr[1], 'ro', label = "Algorithm 1")
    axis[1].plot(numImps, timeArr[2], 'go', label = "Algorithm 2")
    # Labels
    axis[0].set_xlabel('Number of Impressions')
    axis[0].set_ylabel('Objective Value')
    axis[1].set_xlabel('Number of Impressions')
    axis[1].set_ylabel('Time Taken')
    axis[0].legend()
    axis[1].legend()
    plt.tight_layout()
    # Save and Clear
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/ObjTimeVsImps.png')
    plt.cla()
    plt.clf()

def graph(x, y, xlabel, ylabel):
    plt.plot(x, y, 'bo')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('/Users/aravchadha/Documents/GitHub/rise-interns-aene/Images/' + xlabel + 'Vs' + ylabel + '.png')
    plt.cla()
    plt.clf()
