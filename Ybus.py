from System import System
import numpy as np


class Ybus:
    def __init__(self, system: System):
        self.system = system

    def createYbus(self):
        self.yBusMatrix=np.zeros((len(self.system.buses),len(self.system.buses)))




testSystem=System("test")

testSystem.add_tranformer("transformer1", 100, 140, 110, 2, 10, "A", "B")
testSystem.add_transmission_line("line1", 5, "B", "C", 2, 3, 5, 4, 3, 3, 2, 1,3, 3, 2, 1,120)

Ybustest=Ybus(testSystem)

Ybustest.createYbus()
print("good")

