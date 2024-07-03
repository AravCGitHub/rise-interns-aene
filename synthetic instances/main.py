import random
from advertiser import Advertiser
from impression import Impression

def syntheticInstance(numAds, numImps):
    numTypes = 10
    ads = []
    for i in range(numAds):
        ads.append(Advertiser(numTypes))
    imps = []
    for i in range(numImps):
        imps.append(Impression(random.randint(0, numTypes-1)))
    return ads, imps

a, i = syntheticInstance(3,5)

for x in a:
    print(x)
