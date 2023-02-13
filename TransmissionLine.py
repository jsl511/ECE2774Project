import math

from Bus import Bus
from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry


class TransmissionLine:
    def __init__(self, name, length, bus1Connection, bus2Connection, spacing, numberConductors,geometry, conductor,v):
        self.name = name
        self.length = length
        self.v=v
        self.bus1Connection = bus1Connection
        self.bus2Connection = bus2Connection

        self.buses = [self.bus1Connection, self.bus2Connection]

        self.Bundle = None
        self.Geometry = None
        self.conductor = conductor


        self.spacing=spacing
        self.numberConductors=numberConductors

        self.Bundle = Bundle(self.name, self.spacing, self.numberConductors,self.conductor)

        self.geometry=geometry

        self.capacitance = (2 * math.pi * 8.854 * 10 ** (-12)) / math.log(self.geometry.D_eq / self.Bundle.D_SC)
        self.inductance = (2 * 10 ** (-7)) * math.log(self.geometry.D_eq / self.Bundle.D_SL)

        self.impedance = (self.Bundle.resistance*self.length) + 1j*377*(self.inductance*self.length)
        self.admittance = 1/self.impedance #update


        self.shuntAdmittance = 1j*377*(self.capacitance*self.length)


