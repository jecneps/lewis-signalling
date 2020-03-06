from sim import Simulation
from urns import Reinforcement 


reinforcement = Reinforcement(2, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
sim.recordUrnLevels(100, 100, "test.p")
#sim.recordStateAddition(1, 200000, 2, 7,"stateAddition.p")