class Generator:
    def __init__(self, name, bus, power, positive_impedance, negative_impedance, zero_impedance):
        self.name = name
        self.bus = bus
        self.power = power
        self.positive_impedance = positive_impedance
        self.negative_impedance = negative_impedance
        self.zero_impedance = zero_impedance
