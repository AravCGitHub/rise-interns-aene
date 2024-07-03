import random
import math

class Impression:

    def __init__(self,type):
        self.type = type
        self.displayTime = self.getTime()

    def __str__(self):
        return "type: " + str(self.type) + " - Display time:" + str(self.displayTime)

    def getTime(self):
        mean = random.random()
        time = random.gauss(mean,1.5)
        return time