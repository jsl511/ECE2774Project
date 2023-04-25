from math import atan, e


class Transformer:
    def __init__(self, name, power, voltage1, voltage2, z_pu, x_r, bus1, bus2):
        self.name = name
        self.power = power          # rated power (MVA)
        self.voltage1 = voltage1    # high-side voltage rating (kV)
        self.voltage2 = voltage2    # low-side voltage rating (kV)
        self.z_pu = z_pu            # rated impedance (pu)
        self.x_r = x_r              # X/R ratio
        self.bus1 = bus1            # high-side bus connection
        self.bus2 = bus2            # low-side bus connection

        self.impedance = self.z_pu*e**(1j*atan(self.x_r))
        self.admittance = 1/self.impedance
        # print("Transformer " + self.name + " admittance is " + str(self.transformer_admittance))
        # print()
