from math import atan, e


class Transformer:
    def __init__(self, name, power, voltage1, voltage2, z, x_r, bus1, bus2):
        self.name = name
        self.power = power          # rated power (MVA)
        self.voltage1 = voltage1    # high-side voltage rating (kV)
        self.voltage2 = voltage2    # low-side voltage rating (kV)
        self.z = z                  # rated impedance (pu)
        self.x_r = x_r              # X/R ratio
        self.bus1 = bus1            # high-side bus connection
        self.bus2 = bus2            # low-side bus connection

        self.impedance = self.z * e ** (1j * atan(self.x_r))    # transformer impedance, per-unit
        self.admittance = 1/self.impedance                      # transformer admittance, per-unit
        # print("Transformer " + self.name + " admittance is " + str(self.transformer_admittance))
        # print()
