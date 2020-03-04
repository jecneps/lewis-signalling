import pickle

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
                #print(self.model.score())
                return (True, i)
            i = i + 1

        #self.plot()   
        return (False, self.model.score())

    def runUrnLevels(self, limit = None):
        l = []
        i = 0
        while(limit == None or i < limit):
            self.doStep()
            if self.model.stopLearning():
                return (l, True, i)
            i = i + 1
            l.append(self.model.cooperationValues())

        return (l, False, self.model.score())

    def runStateAddition(self, timeTillAdd, nCap):
        i = 0
        timeSinceAdd = i
        startingN = self.model.n
        curN = startingN
        data = []
        indexes = []
        while(curN <= nCap or timeSinceAdd >= timeTillAdd):
            self.doStep()
            i = i + 1
            timeSinceAdd = timeSinceAdd + 1
            data.append(self.model.cooperationValues())

            if self.model.stopLearning() or timeSinceAdd >= timeTillAdd:
                curN = curN + 1
                timeSinceAdd = 0
                self.model.addState()
                indexes.append(i)
                print("added! " + str(i))
        return (data, indexes)

    def recordStateAddition(self, n, timeTillAdd, startN, nCap, fileName):
        results = []
        for i in range(n):
            self.model.reset(startN)
            results.append(self.runStateAddition(timeTillAdd, nCap))
            print(str(i))

        data = dict()
        data["startN"] = startN
        data["nCap"] = nCap
        data["n"] = n
        data["timeTillAdd"] = timeTillAdd
        data["results"] = results
        data["convThreshold"] = self.model.convThreshold
        pickle.dump(data, open(fileName, "wb"))


    def recordSimulations(self, n, cap, fileName):
        results = []
        for i in range(n):
            self.model.reset(self.model.n)
            results.append(self.run(limit = cap))
            print(str(i))


        print(fileName)
        data = dict()
        data["n"] = n
        data["cap"] = cap
        data["convThreshold"] = self.model.convThreshold
        data["results"] = results
        pickle.dump(data, open(fileName, "wb"))

    def recordUrnLevels(self, n, cap, fileName):
        results = []
        for i in range(n):
            self.model.reset(self.model.n)
            results.append(self.runUrnLevels(limit = cap))
            print(str(i))

        print(fileName)
        data = dict()
        data["n"] = n
        data["cap"] = cap
        data["convThreshold"] = self.model.convThreshold
        data["results"] = results
        pickle.dump(data, open(fileName, "wb"))
