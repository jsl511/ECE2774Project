class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        self.voltage = 0
        self.angle = 0
        self.power = 0
        self.reactive = 0

        Bus.bus_count += 1

    def set_voltage(self, voltage, angle):
        self.voltage = voltage
        self.angle = angle

    def set_power(self, power, reactive):
        self.power = power
        self.reactive = reactive