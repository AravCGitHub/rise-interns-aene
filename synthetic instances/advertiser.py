import random
from impression import Impression

class Advertiser:
    
    def __init__(self, numTypes):
        self.budget = random.randint(1, 100)
        self.valuations = []
        self.impressions = [Impression(0)] * self.budget
        self.beta = 0
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
    

    
    
    