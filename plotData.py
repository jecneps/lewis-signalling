import pickle
import numpy as np
import matplotlib.pyplot as plt 



data = pickle.load(open("n4Urns.p", "rb"))

print(data)

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

makeStepHist(data)
makeEVHist(data)

