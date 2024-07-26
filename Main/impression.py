import random

class Impression:
    
    def __init__(self):
        self.displayTime = random.gauss(random.random(),1.5)
        self.weight = 0 # for alg1
        self.number = 0 # for alg1

    def __str__(self):
        return "Number: " + str(self.number) + " Weight: " + str(self.weight)
    
    def __repr__(self):
        return "Number: " + str(self.number) + " Weight: " + str(self.weight)
    
    def weight_key(impression):
        return impression.weight