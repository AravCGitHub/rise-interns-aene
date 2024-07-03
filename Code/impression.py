import random

class Impression:

    def __init__(self,type):
        self.type = type
        self.displayTime = self.getTime()

    def getTime(self):
        mean = random.random()
        time = random.gauss(mean,1.5)
        return time