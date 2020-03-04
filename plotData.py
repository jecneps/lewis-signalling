import pickle
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 



data = pickle.load(open("n2Levels.p", "rb"))


def makeEVHist(data):
	results = data["results"]
	results = list(map(lambda tup : round(100 * tup[1]), 
			filter(lambda tup: tup[0] == False, 
					results)))

	n, bins, patches = plt.hist(results, 20, range=(0,100), facecolor='green', alpha=0.75)
	plt.xlabel("Expected Value (scaled and rounded)")
	plt.ylabel("Number of Simulations")
	plt.title("Histogram of the EV of " + str(len(results)) + " simulations")
	plt.savefig("ev4.png")
	plt.clf()

def makeStepHist(data):
	results = data["results"]
	results = list(map(lambda tup: tup[1],
					filter(lambda tup: tup[0] == True,
							results)))

	n, bins, patches = plt.hist(results, 50)
	plt.clf()
	logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]),len(bins))
	plt.hist(results, bins=logbins, facecolor='green', alpha=0.75)
	plt.xlabel("Steps till convergence")
	plt.xscale("log")
	plt.ylabel("Number of Simulations")
	plt.title("Histogram of the Convergence rates of " + str(len(results)) + " simulations")
	plt.savefig("step4.png")
	plt.clf()

#currently only graphs on simulations worth...
#... need to decide how i want to aggregate
def makeLevelsGraph(data):
	res = data["results"]
	numUrns = len(res[0][0][0])
	states = dict()
	for i in range(numUrns):
		states[i] = list(map(lambda urnMap: round(urnMap[i] * 100),
								res[0][0]))
	d = {"x": range(1, len(states[0]) + 1)}
	print(len(states[0]))
	print(len(states[1]))
	for key in states:
		d["y" + str(key)] = states[key]
		print(len(d["y" + str(key)]))
	#print(d)
	print(len(d["x"]))
	df = pd.DataFrame(d)
	for key in states:
		plt.plot("x", "y" + str(key), data = df)
	plt.savefig("urnLevels.png")

#makeStepHist(data)
#makeEVHist(data)
makeLevelsGraph(data)
