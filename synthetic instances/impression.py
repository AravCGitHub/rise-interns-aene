import random

class Impression:
    
    def __init__(self,type):
        self.type = type
        self.displayTime = self.getTime()

    def __str__(self):
        return "Type: " + str(self.type) + " - Display Time:" + str(self.displayTime)

    def getTime(self):
        mean = random.random()
        time = random.gauss(mean,1.5)
        return time
    
    def returnType(self):
        return self.type