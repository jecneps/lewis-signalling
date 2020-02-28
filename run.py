from sim import Simulation
from urns import Reinforcement 


reinforcement = Reinforcement(4, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
sim.recordSimulations(1000, 1000000, "n4Urns.p")