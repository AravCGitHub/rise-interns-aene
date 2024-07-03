import random

class Advertiser:
    def __init__(self, numTypes):
        self.budget = random.randint(1, 100)
        self.valuation = []
        for i in range(numTypes):
            self.valuation.append(random.expovariate(1))