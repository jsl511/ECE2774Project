class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        self.voltage = None
        self.angle = None
        self.power = None
        self.reactive = None

        Bus.bus_count += 1

    def set_voltage(self, angle, voltage):
        self.angle = angle
        self.voltage = voltage

    def set_power(self, P_G, Q_G, P_L, Q_L):
        self.power = P_G - P_L
        self.reactive = Q_G - Q_L
