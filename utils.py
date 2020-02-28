import random

class Utils(object):
	
    def randWorldState(n):
        x = random.randint(0,n-1)
        return x

    def payout(state, res):
        return 1 if state == res else 0

    def genStrats(n):
    	strats = list(itertools.product(range(n), repeat=n))
    	s = list(itertools.product(strats, repeat=2))
    	return s