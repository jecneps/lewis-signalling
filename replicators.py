import random
import itertools
from collections import namedtuple
from functools import reduce

def genStrats(n):
    strats = list(itertools.product(range(n), repeat=n))
    s = list(itertools.product(strats, repeat=2))
    return s

def randWorldState():
    x = random.randint(0,1)
    return x


strats = genStrats(2)

class Entry(object):
    def __init__(self, pop, fitness):
        self.population = pop
        self.fitness = fitness



#a strat is a tuple
class Agent(object):
    #strat is a tuple of tuples.
    #first tuple indexes the role, second indexs the behavior
    def __init__(self, strat):
        self.strat = strat

    # role is 0 for sender, 1 for reciever
    # info is an int corresponding to the value of the state...
    #... or signal received from the world or other player
    def play(self, role, info):
        return self.strat[role][info]

    


class ReplicatorDynamics(object):

    def __init__(self):
        self.table = dict()
        self.alpha = 10
        for strat in strats:
            self.table[strat] = Entry(10,0)

    def pairs(self):
        weights = list(map(lambda strat: self.table[strat].population,
                      strats))
        stratIndex = [x for x in range(0,len(strats))]
        while (sum(weights) > 1):
            #choice returns a list, so remove index from list
            strat1 = random.choices(stratIndex, weights)[0]
            weights[strat1] = weights[strat1] - 1
            strat2 = random.choices(stratIndex, weights)[0]
            weights[strat2] = weights[strat2] - 1
            yield (Agent(strats[strat1]), Agent(strats[strat2]))

    def recordGame(self, a1, a2, res):
        self.table[a1.strat].fitness = self.table[a1.strat].fitness + res
        self.table[a2.strat].fitness = self.table[a2.strat].fitness + res

    def learn(self):
        meanFitness = self.calcMeanFitness()
        for strat in strats:
            self.table[strat].population = self.calcPopUpdate(strat, meanFitness)
            self.table[strat].fitness = 0 #zero it just in case?

    def calcPopUpdate(self, strat, meanFitness):
        prevPop = self.table[strat].population
        delta = (self.alpha + self.table[strat].fitness) / (self.alpha + meanFitness)
        return round(prevPop * delta)

    def calcMeanFitness(self):
        fitness = reduce(lambda acc, x: acc + x,
                     map(lambda s: self.table[s].fitness,
                         strats),
                     0)
        l = len(list(filter(lambda p: p != 0,
                       map(lambda s: self.table[s].population,
                           strats))))
        return fitness / l

    def plot(self):
        print("Population")
        for strat in strats:
            print(strat)
            print("The above strat has a population of :" + str(self.table[strat].population))

    

class Simulation(object):

    def __init__(self, model):
        self.model = model

    def doStep(self):
        for (a1, a2) in self.model.pairs():
            self.playgame(a1, a2, self.model.recordGame)
        self.model.learn()

    def plot(self):
        self.model.plot()
                   
                   
    def playgame(self, a1, a2, record):
        state = randWorldState()
        res = a2.play(1, a1.play(0, state))
        print("a1=" + str(a1.strat) + ", a2=" + str(a2.strat) + "state=" +str(state) + ", res=" + str(res) + ", pay=" + str(payout(state, res)))
        record(a1, a2, payout(state, res))
        state = randWorldState()
        res = a1.play(1, a2.play(0, state))
        record(a1, a2, payout(state, res))

    def run(self, n):
        for i in range(n):
            self.doStep()
        self.plot()
def payout(state, res):
    return 1 if state == res else 0

replicators = ReplicatorDynamics()
sim = Simulation(replicators)
sim.run(1)





