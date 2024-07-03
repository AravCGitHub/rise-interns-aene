import math
import random
from advertiser import Advertiser
from impression import Impression

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def syntheticInstance(numAds, numImps):
    numTypes = 8
    ads = []
    for i in range(numAds):
        ads.append(Advertiser(numTypes))
    imps = []
    for i in range(numImps):
        sections = (6.0 / numTypes)
        rand = random.gauss(0,1) + 3
        type = clamp(math.floor(0.5 + (rand / sections)), 1, numTypes)
        imps.append(Impression(type))
    return ads, imps

a, i = syntheticInstance(5,3)

for x1 in i:
    print(x1)
for x2 in a:
    print(x2)