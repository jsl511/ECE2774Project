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

    def set_power(self, power, reactive):
        self.power = power
        self.reactive = reactive

    def get_power(self):
        return self.power
