import numpy as np


class Ybus:
    def __init__(self, system):
        self.system = system

        self.y_bus = np.zeros((len(self.system.buses), len(self.system.buses)), dtype=complex)

        # transformer admittance
        for value in self.system.transformers.values():
            bus1 = int(value.bus1) - 1
            bus2 = int(value.bus2) - 1

            self.y_bus[bus1, bus2] -= [value.transformer_admittance]
            self.y_bus[bus1, bus1] += [value.transformer_admittance]
            self.y_bus[bus2, bus2] += [value.transformer_admittance]
            self.y_bus[bus2, bus1] = self.y_bus[bus1, bus2]

        # transmission line admittance
        for value in self.system.lines.values():
            bus1 = int(value.bus1) - 1
            bus2 = int(value.bus2) - 1

            self.y_bus[bus1, bus2] -= [1/value.impedance + value.admittance]
            self.y_bus[bus1, bus1] += [1/value.impedance + value.admittance/2]
            self.y_bus[bus2, bus2] += [1/value.impedance + value.admittance/2]
            self.y_bus[bus2, bus1] = self.y_bus[bus1, bus2]

        # np.set_printoptions(linewidth=200)
        # print("y_bus is: \n" + str(np.around(self.y_bus, decimals=2)))
        # print(np.around(np.absolute(self.y_bus), decimals=2))
        # print(np.around(np.angle(self.y_bus), decimals=2))
