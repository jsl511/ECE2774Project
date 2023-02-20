class Bus:
    bus_count = 0

    def __init__(self, name):
        self.name = name

        Bus.bus_count += 1
        print("There are " + str(Bus.bus_count) + " buses in the system.")
        