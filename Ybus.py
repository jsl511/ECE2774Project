import numpy as np


class Ybus:
    def __init__(self, system):
        self.system = system

        self.y_bus = np.zeros((len(self.system.buses), len(self.system.buses)), dtype=complex)

        # transformer admittance
        for transformer in self.system.transformers.values():
            bus1 = int(transformer.bus1) - 1
            bus2 = int(transformer.bus2) - 1

            self.y_bus[bus1,bus2] -= [transformer.admittance]
            self.y_bus[bus1,bus1] += [transformer.admittance]
            self.y_bus[bus2,bus2] += [transformer.admittance]
            self.y_bus[bus2,bus1] = self.y_bus[bus1,bus2]

        # transmission line admittance
        for line in self.system.lines.values():
            bus1 = int(line.bus1) - 1
            bus2 = int(line.bus2) - 1

            self.y_bus[bus1,bus2] -= [1/line.impedance]
            self.y_bus[bus1,bus1] += [1/line.impedance + line.admittance/2]
            self.y_bus[bus2,bus2] += [1/line.impedance + line.admittance/2]
            self.y_bus[bus2,bus1] = self.y_bus[bus1,bus2]

        # np.set_printoptions(linewidth=200)
        # print("y_bus is: \n" + str(self.y_bus))
        # print()
        # print("y_bus rounded is: \n " + str(np.around(self.y_bus, decimals=2)))
        # print(np.around(np.absolute(self.y_bus), decimals=2))
        # print(np.around(np.angle(self.y_bus), decimals=2))
