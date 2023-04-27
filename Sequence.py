import numpy as np
from math import inf
np.set_printoptions(linewidth=200)


class Sequence:
    def __init__(self, system):
        self.generators = system.generators
        self.transformers = system.transformers
        self.lines = system.lines

        self.z_positive = self.__calculate_positive_sequence(system)
        print(self.z_positive)
        self.z_negative = self.__calculate_negative_sequence(system)
        print(self.z_negative)
        self.z_zero = self.__calculate_zero_sequence(system)
        print(self.z_zero)

    def __calculate_positive_sequence(self, system):
        z_positive = np.zeros((len(system.buses), len(system.buses)), dtype=complex)

        # transformer impedance
        for transformer in self.transformers.values():
            bus1 = int(transformer.bus1) - 1
            bus2 = int(transformer.bus2) - 1

            z_positive[bus1, bus2] -= [transformer.impedance]
            z_positive[bus1, bus1] += [transformer.impedance]
            z_positive[bus2, bus2] += [transformer.impedance]
            z_positive[bus2, bus1] = z_positive[bus1, bus2]

        # transmission line admittance
        for line in self.lines.values():
            bus1 = int(line.bus1) - 1
            bus2 = int(line.bus2) - 1

            z_positive[bus1, bus2] -= [line.impedance]
            z_positive[bus1, bus1] += [line.impedance + 1 / (line.admittance / 2)]
            z_positive[bus2, bus2] += [line.impedance + 1 / (line.admittance / 2)]
            z_positive[bus2, bus1] = z_positive[bus1, bus2]

        for generator in self.generators.values():
            bus = int(generator.bus) - 1

            z_positive[bus, bus] += [generator.positive_impedance]

        return z_positive

    def __calculate_negative_sequence(self, system):
        z_negative = np.zeros((len(system.buses), len(system.buses)), dtype=complex)

        # transformer impedance
        for transformer in self.transformers.values():
            bus1 = int(transformer.bus1) - 1
            bus2 = int(transformer.bus2) - 1

            z_negative[bus1, bus2] -= [transformer.impedance]
            z_negative[bus1, bus1] += [transformer.impedance]
            z_negative[bus2, bus2] += [transformer.impedance]
            z_negative[bus2, bus1] = z_negative[bus1, bus2]

        # transmission line admittance
        for line in self.lines.values():
            bus1 = int(line.bus1) - 1
            bus2 = int(line.bus2) - 1

            z_negative[bus1, bus2] -= [line.impedance]
            z_negative[bus1, bus1] += [line.impedance + 1 / (line.admittance / 2)]
            z_negative[bus2, bus2] += [line.impedance + 1 / (line.admittance / 2)]
            z_negative[bus2, bus1] = z_negative[bus1, bus2]

        for generator in self.generators.values():
            bus = int(generator.bus) - 1

            z_negative[bus, bus] += [generator.negative_impedance]

        return z_negative

    def __calculate_zero_sequence(self, system):
        z_zero = np.zeros((len(system.buses), len(system.buses)), dtype=complex)

        # transformer impedance
        for transformer in self.transformers.values():
            bus1 = int(transformer.bus1) - 1
            bus2 = int(transformer.bus2) - 1

            z_zero[bus1,bus2] -= [transformer.impedance]
            z_zero[bus1,bus1] += [transformer.impedance]
            z_zero[bus2,bus2] += [transformer.impedance]
            z_zero[bus2,bus1] = z_zero[bus1,bus2]

            # hardcoding transformer 1 wye-side grounding
            if bus2 == 1:
                z_zero[bus2,bus2] += 3

            # hardcoding transformer 2 infinite impedance for delta - ungrounded wye
            if (bus1 == 5) and (bus2 == 6):
                z_zero[bus1,bus2] = inf
                z_zero[bus2,bus1] = z_zero[bus1,bus2]

        # transmission line admittance
        for line in self.lines.values():
            bus1 = int(line.bus1) - 1
            bus2 = int(line.bus2) - 1
            
            # zero sequence line impedance is three times positive sequence
            z_zero[bus1, bus2] -= [3 * line.impedance]
            z_zero[bus1, bus1] += [3 * (line.impedance + 1/(line.admittance/2))]
            z_zero[bus2, bus2] += [3 * (line.impedance + 1/(line.admittance/2))]
            z_zero[bus2, bus1] = z_zero[bus1, bus2]

        for generator in self.generators.values():
            bus = int(generator.bus) - 1

            z_zero[bus, bus] += [generator.zero_impedance]

            # this is hardcoding the grounding impedance for generator 2
            if bus == 6:
                z_zero[bus,bus] += 3

        return z_zero
