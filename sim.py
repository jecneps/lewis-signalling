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

    def recordSimulations(self, n, cap, fileName):
        results = []
        for i in range(n):
            self.model.reset()
            results.append(self.run(limit = cap))
            print(str(i))

        print(fileName)
        data = dict()
        data["n"] = n
        data["cap"] = cap
        data["convThreshold"] = self.model.convThreshold
        data["results"] = results
        pickle.dump(data, open(fileName, "wb"))