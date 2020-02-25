import random
import itertools
from collections import namedtuple
from functools import reduce

class UrnAgent(object):

    def __init__(self, n):
        #floats, important
        self.urns = [[1.0 for y in range(n)] for x in range(n)]

    def play(self, info):
        urn = self.urns[info]
        return random.choices(range(len(urn)), urn)[0]

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

    def pairs(self):
        yield (self.sender, self.receiver)

    def learn(self):
        pass

    def plot(self):
        print("Senders urns: ")
        self.sender.printUrns()
        print("receiver urn: ")
        self.receiver.printUrns()

    def normalizeUrn(self, urn):
        s = sum(urn)
        return list(map(lambda x: x/s,
                        urn)
                    )

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
        agent.urns[stimulus] = self.normalizeUrn(urn)

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
        return self.agentConverged(self.sender) and self.agentConverged(self.receiver)
