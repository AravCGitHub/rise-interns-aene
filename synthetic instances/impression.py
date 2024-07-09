import random

class Impression:
    
    def __init__(self,type):
        self.type = type
        self.displayTime = random.gauss(random.random(),1.5)
        self.valWithCurrAdv = 0

    def __str__(self):
        return "Type: " + str(self.type)
    
    def __repr__(self):
        return "Type: " + str(self.type)
    
    def returnType(self):
        return self.type