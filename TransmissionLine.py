import math

from Bus import Bus
from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry


class TransmissionLine:
    def __init__(self, name, length, bus1Connection, bus2Connection):
        self.name = name
        self.length = length
        self.bus1Connection = Bus(bus1Connection)
        self.bus2Connection = Bus(bus2Connection)

        self.Bundle = None
        self.Geometry = None
        self.Conductor = None

        self.impedance = None
        self.admittance = None

    def setBundle(self, name, spacing, numberConductors):
        self.Bundle = Bundle(name, spacing, numberConductors)

    def setGeometry(self, x_a, x_b, x_c, y_a, y_b, y_c):
        self.Geometry = Geometry(x_a, x_b, x_c, y_a, y_b, y_c)

    def solveImpedance(self):
        self.impedance = (self.Bundle.resistance*self.length) + 1j*377*(self.Bundle.inductance*self.length)
        self.admittance = 1/self.admittance

    def solveShuntAdmittance(self):
        self.shuntAdmittance = 1j*377*(self.Bundle.capacitance*self.length)

TX1 = TransmissionLine("line 1",100,"A","B")
TX1.setBundle("two line",2,2)
TX1.Bundle.setConductor("conductor",2,2,2,2)
TX1.Bundle.setGeometry(4,2,6,2,2,2)
TX1.Bundle.solveCapacitance()
TX1.Bundle.solveInductance()
TX1.solveImpedance()
TX1.solveShuntAdmittance()