import random
import itertools
from functools import reduce
from utils import Utils as ut



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

    def __init__(self, n):
        self.table = dict()
        self.alpha = 0
        self.strats = ut.genStrats(n)
        self.n = n
        for strat in self.strats:
            self.table[strat] = Entry(10,0)

    def pairs(self):
        weights = list(map(lambda strat: self.table[strat].population,
                      self.strats))
        stratIndex = [x for x in range(0,len(self.strats))]
        while (sum(weights) > 1):
            #print("weights: " + str(weights))
            #choice returns a list, so remove index from list
            strat1 = random.choices(stratIndex, weights)[0]
            weights[strat1] = weights[strat1] - 1
            strat2 = random.choices(stratIndex, weights)[0]
            weights[strat2] = weights[strat2] - 1
            yield (Agent(self.strats[strat1]), Agent(self.strats[strat2]))

    def recordGame(self, a1, a2, res):
      #  print("prev fitness:" + str(self.table[a1.strat].fitness) + " " + str(self.table[a2.strat].fitness))
        self.table[a1.strat].fitness = self.table[a1.strat].fitness + res
        self.table[a2.strat].fitness = self.table[a2.strat].fitness + res
        #print("new fitness:" + str(self.table[a1.strat].fitness) + " " + str(self.table[a2.strat].fitness))

    def learn(self):
        meanFitness = self.calcMeanFitness()
        for strat in self.strats:
            if self.table[strat].population > 0:
                self.table[strat].population = self.calcPopUpdate(strat, meanFitness)
                self.table[strat].fitness = 0 #zero it just in case?

    def addState(self):
        

    def calcPopUpdate(self, strat, meanFitness):
        prevPop = self.table[strat].population
        delta = (self.alpha + self.calcStratFitness(strat)) / (self.alpha + meanFitness)
        return round(prevPop * delta)

    def calcMeanFitness(self):
        fitness = sum(map(lambda s: self.table[s].fitness,
                         self.strats))
        numOfAgents = sum(map(lambda s: self.table[s].population,
                            self.strats)) 
        return fitness / numOfAgents

    def calcStratFitness(self, strat):
        return self.table[strat].fitness / self.table[strat].population

    def playGame(self, a1, a2):
        state = ut.randWorldState(self.n)
        res = a2.play(1, a1.play(0, state))
       # print("a1=" + str(a1.strat) + ", a2=" + str(a2.strat) + "state=" +str(state) + ", res=" + str(res) + ", pay=" + str(payout(state, res)))
        self.recordGame(a1, a2, ut.payout(state, res))
        state = ut.randWorldState(self.n)
        res = a1.play(1, a2.play(0, state))
        #print("a2=" + str(a2.strat) + ", a1=" + str(a1.strat) + "state=" +str(state) + ", res=" + str(res) + ", pay=" + str(payout(state, res)))
        self.recordGame(a1, a2, ut.payout(state, res))

    def plot(self):
        print("Population")
        for strat in self.strats:
            print(strat)
            print("The above strat has a population of :" + str(self.table[strat].population))

    def stopLearning(self):
        return len(list(filter(lambda pop: pop > 0,
                            map(lambda strat: self.table[strat].population,
                                self.strats)))) == 1

    









