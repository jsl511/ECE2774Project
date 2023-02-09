import math

from Conductor import Conductor
from Geometry import Geometry


class Bundle:
    def __init__(self, name, spacing, numberConductors):
        self.name = name
        self.spacing = spacing
        self.numberConductors = numberConductors

        self.Conductor = None
        self.Geometry = None

        self.D_SL = None
        self.D_SC = None
        self.resistance = None
        self.capacitance = None
        self.inductance = None

    def setConductor(self, name, diameter, GMR, resistance, ampacity):
        self.Conductor = Conductor(name, diameter, GMR, resistance, ampacity)

        # calculate bundle parameters based on the number of conductors: D_SL, D_SC, resistance per unit length
        if self.numberConductors == 1:
            self.D_SL = self.Conductor.GMR
            self.D_SC = self.Conductor.radius
            self.resistance = self.Conductor.resistance
        elif self.numberConductors == 2:
            self.D_SL = math.sqrt(self.Conductor.GMR * self.spacing)
            self.D_SC = math.sqrt(self.Conductor.radius * self.spacing)
            self.resistance = self.Conductor.resistance / 2
        elif self.numberConductors == 3:
            self.D_SL = (self.Conductor.GMR * (self.spacing ** 2)) ** (1 / 3)
            self.D_SC = (self.Conductor.radius * (self.spacing ** 2)) ** (1 / 3)
            self.resistance = self.Conductor.resistance / 3
        elif self.numberConductors == 4:
            self.D_SL = 1.0941 * (self.Conductor.GMR * (self.spacing ** 3)) ** (1 / 4)
            self.D_SC = 1.0941 * (self.Conductor.radius * (self.spacing ** 3)) ** (1 / 4)
            self.resistance = self.Conductor.resistance / 4
        else:
            print("Invalid number of conductors")
            exit(1)

    def setGeometry(self, x_a, x_b, x_c, y_a, y_b, y_c):
        self.Geometry = Geometry(x_a, x_b, x_c, y_a, y_b, y_c)

    def solveCapacitance(self):
        self.capacitance = (2*math.pi*8.854*10**(-12))/math.log(self.Geometry.D_eq/self.D_SC)

    def solveInductance(self):
        self.inductance = (2*10**(-7))*math.log(self.Geometry.D_eq/self.D_SL)
