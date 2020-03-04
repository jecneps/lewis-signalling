from sim import Simulation
from urns import Reinforcement 


reinforcement = Reinforcement(3, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
sim.recordUrnLevels(100, 1000000, "n3UrnLevels.p")