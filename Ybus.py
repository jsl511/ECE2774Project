import numpy as np


class Ybus:
    def __init__(self):
        self.y_bus = None

    def calculate_Ybus(self, system):
        self.y_bus = np.zeros((len(system.buses), len(system.buses)), dtype=complex)

        # transformer admittance
        for value in system.transformers.values():
            bus1 = int(value.bus1) - 1
            bus2 = int(value.bus2) - 1

            self.y_bus[bus1, bus2] -= [value.transformer_admittance]
            self.y_bus[bus1, bus1] += [value.transformer_admittance]
            self.y_bus[bus2, bus2] += [value.transformer_admittance]
            self.y_bus[bus2, bus1] = self.y_bus[bus1, bus2]

        # transmission line admittance
        for value in system.lines.values():
            bus1 = int(value.bus1) - 1
            bus2 = int(value.bus2) - 1

            self.y_bus[bus1, bus2] -= [1/value.impedance + value.admittance]
            self.y_bus[bus1, bus1] += [1/value.impedance + value.admittance/2]
            self.y_bus[bus2, bus2] += [1/value.impedance + value.admittance/2]
            self.y_bus[bus2, bus1] = self.y_bus[bus1, bus2]

        print(np.around(self.y_bus, decimals=2))

# check connection from bus A to B
    # if connected, through transmission line or transformer?
