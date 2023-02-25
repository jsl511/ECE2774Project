class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        Bus.bus_count += 1
