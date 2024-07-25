import random

class Impression:
    
    def __init__(self,type):
        self.type = type
        self.displayTime = random.gauss(random.random(),1.5)
        self.valWithCurrAdv = 0
        self.weight = 0
        self.number = 0

    def __str__(self):
        return "Type: " + str(self.type) + " Weight: " + str(self.weight)
    
    def __repr__(self):
        return "Type: " + str(self.type) + " Weight: " + str(self.weight)
    
    def returnType(self):
        return self.type
    
    def weight_key(impression):
        return impression.weight