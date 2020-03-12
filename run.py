from sim import Simulation
from urns import Reinforcement 


reinforcement = Reinforcement(2, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
print("levels for 2")
sim.recordUrnLevels(100, 100000, "u2Levels.p")

reinforcement = Reinforcement(3, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
print("levels for 3")
sim.recordUrnLevels(100, 100000, "u3Levels.p")

reinforcement = Reinforcement(4, 0.99)
sim = Simulation(reinforcement)
#sim.run(10000)
print("levels for 4")
sim.recordUrnLevels(100, 100000, "u4Levels.p")
#sim.recordStateAddition(1, 200000, 2, 7,"stateAddition.p")
#sim.recordSimulations(1000, 1000000, "n7Urns.p")
