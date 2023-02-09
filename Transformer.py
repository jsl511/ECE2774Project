import math
from Bus import Bus


class Transformer:
    def __init__(self, name, powerRating, voltageRatingHigh, voltageRatingLow, impedance, xR, bus1Connection, bus2Connection):
        self.name = name
        self.powerRating = powerRating
        self.voltageRatingHigh = voltageRatingHigh
        self.voltageRatingLow = voltageRatingLow
        self.impedance = impedance  # per-unit impedance
        self.xR = xR
        self.bus1Connection = Bus(bus1Connection)
        self.bus2Connection = Bus(bus2Connection)

        self.Impedance = self.impedance*math.e**(1j*math.atan(self.xR))
        self.Admittance = 1/self.Impedance
