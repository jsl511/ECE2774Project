import numpy as np
import math
np.set_printoptions(threshold=np.inf)


class PowerFlow:
    def __init__(self, system, y_bus, slack_bus):
        self.system = system
        self.Y_bus = np.absolute(y_bus)
        self.theta = np.angle(y_bus)
        self.N = len(self.system.buses)     # number of buses (includes the slack bus)

        # voltage and power vectors for power flow
        self.x = np.ones(2 * self.N)
        self.y = np.ones(2 * self.N)

        # initialize y vector with bus powers
        for k in range(self.N):         # for k from 0 to 7 (for loops count up to, not including)
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
        # step 1: update the y vector using start data
        for k in range(self.N):
            P, Q = 0, 0

            for n in range(self.N):
                P += self.Y_bus[k,n] * self.x[n + self.N] * math.cos(self.x[k] - self.x[n] - self.theta[k,n])
                Q += self.Y_bus[k,n] * self.x[n + self.N] * math.sin(self.x[k] - self.x[n] - self.theta[k,n])

            # print(cos)
            # print(sin)
            # print("k = " + str(k) + "\n")
            self.y[k] -= self.x[k + self.N] * P
            self.y[k + self.N] -= self.x[k + self.N] * Q

        print(np.around(self.y, decimals=2))