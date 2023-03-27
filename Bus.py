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

    def set_power(self, generator_power, generator_reactive, load_power, load_reactive):
        self.power = generator_power - load_power
        self.reactive = generator_reactive - load_reactive
