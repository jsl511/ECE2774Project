import numpy as np
from math import cos, sin

np.set_printoptions(linewidth=200)


class PowerFlow:
    def __init__(self, system, y_bus, slack_bus):
        self.system = system
        self.Y_bus = np.absolute(y_bus)
        self.theta = np.angle(y_bus)
        self.N = len(self.system.buses)     # number of buses (includes the slack bus)
        self.slack_bus = slack_bus
        # print("N is equal to: " + str(self.N))
        # print("Y_bus is: \n" + str(np.around(self.Y_bus, decimals=2)))
        # print("theta is: \n" + str(np.around(self.theta, decimals=2)))
        # voltage and power vectors for power flow
        self.x = np.empty(2 * self.N)
        self.y = np.empty(2 * self.N)

        # create uninitialized jacobian quadrants
        self.jacobian1 = np.zeros((self.N, self.N))
        self.jacobian2 = np.zeros((self.N, self.N))
        self.jacobian3 = np.zeros((self.N, self.N))
        self.jacobian4 = np.zeros((self.N, self.N))

        # initialize y vector with bus powers
        for k in range(self.N):             # for k from 0 to 7 (for loops count up to, not including)
            if (k + 1) == self.slack_bus:   # the slack bus has no power ratings (?)
                self.y[k] = None
                self.y[k + self.N] = None
            else:
                self.y[k] = self.system.buses.get(str(k + 1)).power
                self.y[k + self.N] = self.system.buses.get(str(k + 1)).reactive

    def flat_start(self):
        for k in range(self.N):
            self.system.buses.get(str(k + 1)).set_voltage(0, 1.0)
            self.x[k] = self.system.buses.get(str(k + 1)).angle
            self.x[k + self.N] = self.system.buses.get(str(k + 1)).voltage

        # print("x is equal to: " + str(self.x))

    def solve_newton_raphson(self):
        # step 1: update the y vector using start data
        for k in range(self.N):
            P, Q = 0, 0

            for n in range(self.N):
                P += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                Q += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])

            self.y[k] -= self.x[k + self.N] * P
            self.y[k + self.N] -= self.x[k + self.N] * Q

        # print(np.around(self.y, decimals=2))

    def solve_jacobian(self):
        for k in range(self.N):
            j1, j2, j3, j4 = 0, 0, 0, 0  # hold the summations in the diagonal elements

            for n in range(self.N):
                j2 += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                j4 += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])

                if n != k:
                    j1 += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])
                    j3 += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])

                    self.jacobian1[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])
                    self.jacobian2[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                    self.jacobian3[k,n] = -1 * self.x[k + self.N] * self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                    self.jacobian4[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * sin(self.x[k] - self.x[n] - self.theta[k,n])

            self.jacobian1[k,k] = -1 * self.x[k + self.N] * j1
            self.jacobian2[k,k] = self.x[k + self.N] * self.Y_bus[k,k] * cos(self.theta[k,k]) + j2
            self.jacobian3[k,k] = self.x[k + self.N] * j3
            self.jacobian4[k,k] = -1 * self.x[k + self.N] * self.Y_bus[k,k] * sin(self.theta[k,k]) + j4

        # print("The Jacobian for quadrants 1 is: \n" + str(np.around(self.jacobian1, decimals=2)))
        # print("The Jacobian for quadrants 2 is: \n" + str(np.around(self.jacobian2, decimals=2)))
        # print("The Jacobian for quadrants 3 is: \n" + str(np.around(self.jacobian3, decimals=2)))
        # print("The Jacobian for quadrants 4 is: \n" + str(np.around(self.jacobian4, decimals=2)))

    def remove_slack_bus(self):
        pass

    def remove_pv_bus(self, pv_bus):
        pass
