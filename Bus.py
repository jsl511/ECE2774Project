class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        self.voltage = 0
        self.angle = 0
        self.power = 0
        self.reactive = 0

        Bus.bus_count += 1

    def set_voltage(self, angle, voltage):
        self.angle = angle
        self.voltage = voltage
        
    def set_power(self, P_G, Q_G, P_L, Q_L):
        self.power = P_G - P_L
        self.reactive = Q_G - Q_L
