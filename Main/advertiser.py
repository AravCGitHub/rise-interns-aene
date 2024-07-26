import random
import math
import sys
from impression import Impression
from sortedcontainers import SortedList

class Advertiser:
    
    def __init__(self, budget = random.randint(1, 100)):
        self.budget = budget
        self.impressions = SortedList(key=Impression.weight_key)

    def capValuation(self, val):
        max = (math.log(sys.float_info.max) + 1) * 0.25
        if val > max:
            return max
        else:
            return val

    def __str__(self):
        return "Budget: " + str(self.budget)

    def __repr__(self):
        return "Budget: " + str(self.budget)