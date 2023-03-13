class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        self.voltage = None
        self.angle = None
        self.power = None
        self.reactive = None

        Bus.bus_count += 1

    def set_voltage(self, voltage, angle):
        self.voltage = voltage
        self.angle = angle

    def set_power(self, power, reactive):
        self.power = power
        self.reactive = reactive
