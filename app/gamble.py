import random
from datetime import datetime

class Gamble_cl(object):
    def __init__(self):
        self.seed = ""
        self.createSeed()
    def createSeed(self):
        a = datetime.now()
        self.seed = str(hash(random.randint(999999999999,999999999999999999))) +  str(hash(a.microsecond))
        return self.seed
    def setSeed(self, seed):
        self.seed = seed
    def gamble(self):
        if self.seed == "":
            print("error")
            return -1
        print(self.seed)
        random.seed(self.seed)
        Z = random.random()
        print(Z)
        if Z == 0.777:
            print("Jackpot Win")
            return 777
        elif Z > 0.52:
            print("win")
            return 1
        elif Z <= 0.52:
            print("loss")
            return 0
        else:
            print("error")
            return -1        
