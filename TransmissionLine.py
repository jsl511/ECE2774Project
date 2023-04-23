from math import log, pi

# TODO change to pu


class TransmissionLine:
    def __init__(self, name, length, bus1, bus2, bundle, geometry):
        self.name = name
        self.length = length        # (mi)
        self.bus1 = bus1
        self.bus2 = bus2

        self.bundle = bundle        # Bundle object
        self.geometry = geometry    # Geometry object

        self.capacitance = (2*pi*8.854*10**(-12))/log(self.geometry.D_eq/self.bundle.D_SC)    # (F/m)
        self.capacitance = self.capacitance / 0.000621371                                               # convert from (F/m) to (F/mi)

        self.inductance = (2*10**(-7))*log(self.geometry.D_eq/self.bundle.D_SL)                    # (H/m)
        self.inductance = self.inductance / 0.000621371                                                 # convert from (H/m) to (H/mi)

        self.impedance = ((self.bundle.resistance*self.length) + 1j*377*(self.inductance*self.length)) / 529    # series impedance (Ohm)
        # print("Line " + self.name + " impedance is " + str(self.impedance))
        self.admittance = 1j*377*(self.capacitance*self.length) / (1/529)                               # shunt admittance (S)
        # print("Line " + self.name + " admittance is " + str(self.admittance))

    # TODO: functionize conversion between meters and miles
