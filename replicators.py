import random
import itertools
from collections import namedtuple
from functools import reduce
import pickle

def genStrats(n):
    strats = list(itertools.product(range(n), repeat=n))
    s = list(itertools.product(strats, repeat=2))
    return s

def genSingleStrats(n):
    return list(itertools.product(range(n), repeat=n))

singleStrats = genSingleStrats(2)


def randWorldState(n):
    x = random.randint(0,n-1)
    return x


strats = genStrats(4)

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

class UrnAgent(object):

    def __init__(self, n):
        #floats, important
        self.urns = [[1.0 for y in range(n)] for x in range(n)]

    def play(self, info):
        urn = self.urns[info]
        return random.choices(range(len(urn)), self.normalizeUrn(urn))[0]

    def normalizeUrn(self, urn):
        s = sum(urn)
        return list(map(lambda x: x/s,
                        urn)
                    )

    def urnFormat(self, urn):
        return "[" + "%8.4f," * len(urn) + "]"

    def printUrns(self):
        for i, urn in enumerate(self.urns):
            f = "stim: " + str(i) + " , " + self.urnFormat(urn)
            print(f %tuple(urn))

class Reinforcement(object):
    
    def __init__(self, n):
        self.sender = UrnAgent(n)
        self.receiver = UrnAgent(n)
        self.n = n
        self.convThreshold = 0.999

    def reset(self):
        self.sender = UrnAgent(self.n)
        self.receiver = UrnAgent(self.n)

    def pairs(self):
        yield (self.sender, self.receiver)

    def learn(self):
        pass

    def plot(self):
        print("Senders urns: ")
        self.sender.printUrns()
        print("receiver urn: ")
        self.receiver.printUrns()
        print("With the expected value of " + str(self.calculateExpectedValue(self.sender, self.receiver)))
        

    def playGame(self, sender, receiver):
        state = randWorldState(self.n)
        signal = sender.play(state)
        action = receiver.play(signal)
        #print("state: " + str(state) + " signal: " + str(signal) + " action: " + str(action))
        if payout(state, action) == 1:
            self.updateUrn(sender, state, signal)
            self.updateUrn(receiver, signal, action)

    def updateUrn(self, agent, stimulus, result):
        urn = agent.urns[stimulus]
        urn[result] = urn[result] + 1

    def urnHasConverged(self, urn):
        return len(list(filter(lambda p: p > self.convThreshold,
                            urn))) == 1

    def agentConverged(self, agent):
        return reduce(lambda acc, b: b and acc,
                        map(lambda urn: self.urnHasConverged(urn),
                            agent.urns),
                        True
                        )

    def stopLearning(self):
        return self.score() >= self.convThreshold


    def score(self):
        return self.calculateExpectedValue(self.sender, self.receiver)

    def calculateExpectedValue(self, sender, receiver):
        ev = 0
        for state, senderUrn in enumerate(sender.urns):
            stateEV = 0
            for signal, probOfSend in enumerate(sender.normalizeUrn(senderUrn)):
                receiverUrn = receiver.urns[signal]
                sigEV = 0
                for action, probOfDo in enumerate(receiver.normalizeUrn(receiverUrn)):
                    sigEV = sigEV + probOfDo * payout(state, action)
                stateEV = stateEV + sigEV * probOfSend

            ev = ev + stateEV * (1 / self.n)
        return ev





class ReplicatorDynamics(object):

    def __init__(self, n):
        self.table = dict()
        self.alpha = 0
        self.n = n
        for strat in strats:
            self.table[strat] = Entry(10,0)

    def pairs(self):
        weights = list(map(lambda strat: self.table[strat].population,
                      strats))
        stratIndex = [x for x in range(0,len(strats))]
        while (sum(weights) > 1):
            #print("weights: " + str(weights))
            #choice returns a list, so remove index from list
            strat1 = random.choices(stratIndex, weights)[0]
            weights[strat1] = weights[strat1] - 1
            strat2 = random.choices(stratIndex, weights)[0]
            weights[strat2] = weights[strat2] - 1
            yield (Agent(strats[strat1]), Agent(strats[strat2]))

    def recordGame(self, a1, a2, res):
      #  print("prev fitness:" + str(self.table[a1.strat].fitness) + " " + str(self.table[a2.strat].fitness))
        self.table[a1.strat].fitness = self.table[a1.strat].fitness + res
        self.table[a2.strat].fitness = self.table[a2.strat].fitness + res
        #print("new fitness:" + str(self.table[a1.strat].fitness) + " " + str(self.table[a2.strat].fitness))

    def learn(self):
        meanFitness = self.calcMeanFitness()
        for strat in strats:
            if self.table[strat].population > 0:
                self.table[strat].population = self.calcPopUpdate(strat, meanFitness)
                self.table[strat].fitness = 0 #zero it just in case?

    def calcPopUpdate(self, strat, meanFitness):
        prevPop = self.table[strat].population
        delta = (self.alpha + self.calcStratFitness(strat)) / (self.alpha + meanFitness)
        return round(prevPop * delta)

    def calcMeanFitness(self):
        fitness = sum(map(lambda s: self.table[s].fitness,
                         strats))
        numOfAgents = sum(map(lambda s: self.table[s].population,
                            strats)) 
        return fitness / numOfAgents

    def calcStratFitness(self, strat):
        return self.table[strat].fitness / self.table[strat].population

    def playGame(self, a1, a2):
        state = randWorldState(self.n)
        res = a2.play(1, a1.play(0, state))
       # print("a1=" + str(a1.strat) + ", a2=" + str(a2.strat) + "state=" +str(state) + ", res=" + str(res) + ", pay=" + str(payout(state, res)))
        self.recordGame(a1, a2, payout(state, res))
        state = randWorldState(self.n)
        res = a1.play(1, a2.play(0, state))
        #print("a2=" + str(a2.strat) + ", a1=" + str(a1.strat) + "state=" +str(state) + ", res=" + str(res) + ", pay=" + str(payout(state, res)))
        self.recordGame(a1, a2, payout(state, res))

    def plot(self):
        print("Population")
        for strat in strats:
            print(strat)
            print("The above strat has a population of :" + str(self.table[strat].population))

    def stopLearning(self):
        return len(list(filter(lambda pop: pop > 0,
                            map(lambda strat: self.table[strat].population,
                                strats)))) == 1

    

class Simulation(object):

    def __init__(self, model):
        self.model = model

    def doStep(self):
        for (a1, a2) in self.model.pairs():
            self.model.playGame(a1, a2)
        self.model.learn()

    def plot(self):
        self.model.plot()    

    def run(self, limit = None):
        i = 0
        while(limit == None or i < limit):
            self.doStep()
            if self.model.stopLearning():
                print(self.model.score())
                return (True, i)
            i = i + 1

        self.plot()   
        return (False, self.model.score())

    def recordSimulations(self, n, cap, fileName):
        results = []
        for i in range(n):
            self.model.reset()
            results.append(self.run(limit = cap))

        print(fileName)
        pickle.dump(results, open(fileName, "wb"))


def payout(state, res):
    return 1 if state == res else 0

replicators = ReplicatorDynamics(4)
reinforcement = Reinforcement(8)
sim = Simulation(reinforcement)
sim.run(100000)
#sim.recordSimulations(20, 10000, "simdata.p")





