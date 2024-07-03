import random
import advertiser
import impression.py

def syntheticInstance(numAds, numImps):
    numTypes = 10
    ads = []
    for i in range(numAds):
        ads.append(advertiser.Advertiser(numTypes))
    imps = []
    for i in range(numImps):
        imps.append(impression.Impression(random.randint(0, numTypes-1)))
    return ads, imps

print(syntheticInstance(3,5))
