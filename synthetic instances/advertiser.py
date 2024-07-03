import random

class Advertiser:
    def __init__(self, numTypes):
        self.budget = random.randint(1, 100)
        self.valuation = []
        for i in range(numTypes):
            self.valuation.append(random.expovariate(1))

    def __str__(self):
        return "Budget: " + str(self.budget) + " - Valuations:" + str(self.valuation)