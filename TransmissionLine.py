import math

from Bundle import bundle
from Geometry import geometry


class TransmissionLine:
    def __init__(self, name, length, bus1, bus2, bundle, geometry):
        self.name = name
        self.length = length    # (mi)
        self.bus1 = bus1
        self.bus2 = bus2

        self.bundle = bundle        # Bundle object
        self.geometry = geometry    # Geometry object

        self.inductance = None      # (H/m)
        self.capacitance = None     # (F/m)
        self.impedance = None       # series impedance of the line (Ohms)
        self.admittance = None      # shunt admittance of the line (S)

    def calculate_capacitance(self):
        self.capacitance = (2*math.pi*8.854*10**(-12))/math.log(self.geometry.D_eq/self.bundle.D_SC)
        self.capacitance = self.capacitance/0.000621371     # convert from (F/m) to (F/mi)

    def calculate_inductance(self):
        self.inductance = (2*10**(-7))*math.log(self.geometry.D_eq/self.bundle.D_SL)
        self.inductance = self.inductance/0.000621371       # convert from (H/m) to (H/mi)

    def calculate_impedance(self):
        self.impedance = (self.bundle.resistance*self.length) + 1j*377*(self.inductance*self.length)

    def calculate_admittance(self):
        self.admittance = 1j*377*(self.capacitance*self.length)


bundle.calculate_GMR()
geometry.calculate_GMD()

TX1 = TransmissionLine("L1", 10, "2", "4", bundle, geometry)
TX1.calculate_capacitance()
print(TX1.capacitance)
TX1.calculate_inductance()
print(TX1.inductance)
TX1.calculate_impedance()
print(TX1.impedance)
TX1.calculate_admittance()
print(TX1.admittance)
