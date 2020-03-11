from sim import Simulation
from urns import Reinforcement 


reinforcement = Reinforcement(7, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
#sim.recordUrnLevels(100, 100000, "test.p")
#sim.recordStateAddition(1, 200000, 2, 7,"stateAddition.p")
sim.recordSimulations(1000, 1000000, "n7Urns.p")
