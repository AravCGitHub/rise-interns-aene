import random
from sortedcontainers import SortedList
from impression import Impression
import math
import sys

class Advertiser:
    
    def __init__(self, numTypes, bud):
        self.budget = bud
        self.valuations = []
        self.impressions = SortedList(key=Impression.weight_key) # for alg1
        for x in range(numTypes):
            self.valuations.append(random.expovariate(1))

    def __str__(self):
        # return "Budget: " + str(self.budget)
        return "vals " + str(self.valuations) + " budget " + str(self.budget)

    def __repr__(self):
        return "vals " + str(self.valuations) + " budget " + str(self.budget)