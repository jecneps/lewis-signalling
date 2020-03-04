import pickle
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt 
import pandas as pd 



data = pickle.load(open("stateAddition.p", "rb"))


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
	for key in states:
		d["y" + str(key)] = states[key]

	df = pd.DataFrame(d)
	for key in states:
		plt.plot("x", "y" + str(key), data = df)
	plt.savefig("urnLevels.png")


def plotStateAddition(data):
	res = data["results"]
	bigList = res[0][0]
	print(res[0][1])
	seriesByState = dict()
	for i in range(data["nCap"]):
		seriesByState[i] = list(map(lambda urn: 0 if i >= len(urn) else urn[i] ,
								bigList))

	d = {"x": range(1, len(seriesByState[0]) + 1)}
	for key in seriesByState:
		d["y" + str(key)] = seriesByState[key]

	df = pd.DataFrame(d)
	for key in seriesByState:
		plt.plot("x", "y" + str(key), data=df)
	plt.savefig("stateAddition2.png")



#makeStepHist(data)
#makeEVHist(data)
#makeLevelsGraph(data)
plotStateAddition(data)
