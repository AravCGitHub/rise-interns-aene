import random
from sortedcontainers import SortedList
from impression import Impression
import math
import sys

class Advertiser:
    
    def __init__(self, numTypes, corruptNum):
        self.budget = random.randint(1, 100)
        self.valuations = []
        self.impressions = SortedList(key=Impression.weight_key) # for alg1
        if corruptNum == 1:
            self.corruption1(numTypes)
        elif corruptNum == 2:
            self.corruption2(numTypes)
        else:
            self.noCorruption(numTypes)
        

    def noCorruption(self, numTypes):
        for x in range(numTypes):
            self.valuations.append(random.expovariate(1))

    def corruption1(self, numTypes):
        for i in range(numTypes):
            temp = random.expovariate(1)
            rand = random.randint(1, 100)
            if rand <= 10:
                temp /= 10
            elif rand <= 20:
                temp /= 100
            self.valuations.append(self.capValuation(temp))

    def corruption2(self, numTypes):
        for i in range(numTypes):
            rand = random.randint(1,2)
            if rand == 1:
                self.valuations.append(0)
            else:
                self.valuations.append(random.expovariate(1)) 

    def capValuation(self, val):
        max = (math.log(sys.float_info.max) + 1) * 0.25
        if val > max:
            return max
        else:
            return val

    def __str__(self):
        # return "Budget: " + str(self.budget)
        return "vals " + str(self.valuations)

    def __repr__(self):
        return "vals " + str(self.valuations)
    
    def returnBudget(self):
        return self.budget
    
    def returnValuation(self):
        return self.valuations
    
    def returnBeta(self):
        return self.beta
    
    def returnImpressions(self):
        return self.impressions
    
# Ways to corrupt instances:
   
# Randomly multiply/divide valuations by 100
# Remove random edges
# Coin flip between exponential and uniform distribution (or any other distribution)
# Randomly change random.expovariate(1) to random.expovariate(10 or 100)