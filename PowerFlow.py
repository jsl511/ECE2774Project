import numpy as np


class PowerFlow:
    def __init__(self, system, y_bus, slack_bus):
        self.system = system
        self.ybus = y_bus
        self.N = len(self.system.buses)     # number of buses (includes the slack bus)

        # voltage and power vectors for power flow
        self.x = np.empty(2 * self.N)
        self.y = np.empty(2 * self.N)

        # initialize y vector with bus powers
        for k in range(self.N):         # for k from 0 to 6 (for loops count up to, not including)
            if (k + 1) == slack_bus:    # the slack bus has no power ratings (?)
                self.y[k] = None
                self.y[k + self.N] = None
            else:
                self.y[k] = self.system.buses.get(str(k + 1)).power
                self.y[k + self.N] = self.system.buses.get(str(k + 1)).reactive

    def flat_start(self):
        for k in range(self.N):
            self.x[k] = 0
            self.x[k + self.N] = 1.0

            # initialize bus object voltages using x data
            self.system.buses.get(str(k + 1)).set_voltage(self.x[k], self.x[k + self.N])

    def solve_newton_raphson(self):
        # step 1: compute the updated y vector using start data
        pass
