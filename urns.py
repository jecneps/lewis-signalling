import random
import itertools
from collections import namedtuple
from functools import reduce
from utils import Utils as ut

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

    def addState(self):
        n = len(self.urns)
        #the new slot should have 1/(n+1) prob of being picked
        for urn in self.urns:
            urn.append(round(sum(urn) / (n)))
        self.urns.append([1.0 for x in range(n + 1)])

    def urnFormat(self, urn):
        return "[" + "%8.4f," * len(urn) + "]"

    def printUrns(self):
        for i, urn in enumerate(self.urns):
            f = "stim: " + str(i) + " , " + self.urnFormat(urn)
            print(f %tuple(self.normalizeUrn(urn)))

class Reinforcement(object):
    
    def __init__(self, n, convThreshold):
        self.sender = UrnAgent(n)
        self.receiver = UrnAgent(n)
        self.n = n
        self.convThreshold = convThreshold

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
        state = ut.randWorldState(self.n)
        signal = sender.play(state)
        action = receiver.play(signal)
        #print("state: " + str(state) + " signal: " + str(signal) + " action: " + str(action))
        if ut.payout(state, action) == 1:
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


    def calculateStateEV(self, sender, receiver, state, senderUrn):
        stateEV = 0
        for signal, probOfSend in enumerate(sender.normalizeUrn(senderUrn)):
            receiverUrn = receiver.urns[signal]
            sigEV = 0
            for action, probOfDo in enumerate(receiver.normalizeUrn(receiverUrn)):
                sigEV = sigEV + probOfDo * ut.payout(state, action)
            stateEV = stateEV + sigEV * probOfSend

        return stateEV

    def calculateExpectedValue(self, sender, receiver):
        ev = 0
        for state, senderUrn in enumerate(sender.urns):
            #print(state)
            stateEV = self.calculateStateEV(sender, receiver, state, senderUrn)
            #print("state ev: " + str(stateEV))
            ev = ev + stateEV * (1 / self.n)
            #print(ev)
        return ev

    def cooperationValues(self):
        return list(map(lambda tup: self.calculateStateEV(self.sender, 
                                                                        self.receiver,
                                                                         tup[0],
                                                                          tup[1]),
                        enumerate(self.sender.urns)))

