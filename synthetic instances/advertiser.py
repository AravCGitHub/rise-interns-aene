import random
from impression import Impression

class Advertiser:
    
    def __init__(self, numTypes, isCorrupted):
        self.budget = random.randint(1, 100)
        self.valuations = []
        self.impressions = [Impression(0)] * self.budget
        self.beta = 0
        if isCorrupted:
            for i in range(numTypes):
                temp = random.expovariate(1)
                rand = random.randint(1, 100)
                if rand <= 5:
                    temp *= 10
                elif rand <= 10:
                    temp /= 10
                self.valuations.append(temp)
        else:
            for i in range(numTypes):
                self.valuations.append(random.expovariate(1))

    def __str__(self):
        return "Budget: " + str(self.budget)
    
    def returnBudget(self):
        return self.budget
    
    def returnValuation(self):
        return self.valuations
    
    def returnBeta(self):
        return self.beta
    
    def returnImpressions(self):
        return self.impressions
    

    
    
    