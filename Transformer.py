import math


class Transformer:
    def __init__(self, name, power, voltage1, voltage2, impedance, x_r, bus1, bus2):
        self.name = name
        self.power = power          # rated power (MVA)
        self.voltage1 = voltage1    # high-side voltage rating (kV)
        self.voltage2 = voltage2    # low-side voltage rating (kV)
        self.impedance = impedance  # rated impedance (pu)
        self.x_r = x_r              # X/R ratio
        self.bus1 = bus1            # high-side bus connection
        self.bus2 = bus2            # low-side bus connection
        
        self.transformer_impedance = None

    def calculate_impedance(self):
        self.transformer_impedance = self.impedance*math.e**(1j*math.atan(self.x_r))
