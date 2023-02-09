class Bus:
    busCount = 0

    def __init__(self, name):
        self.name = name
        self.index = Bus.busCount

        self.voltage = None

        Bus.busCount = Bus.busCount + 1

    def setVoltage(self, voltage):
        self.voltage = voltage
