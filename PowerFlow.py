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
        self.removed_buses = 0              # tracks buses (slack and pv) removed from x, y, and J

        # voltage and power vectors for power flow
        self.x = np.empty(2 * self.N)
        self.y = np.empty(2 * self.N)

        # create uninitialized jacobian quadrants
        self.jacobian1 = np.zeros((self.N, self.N))
        self.jacobian2 = np.zeros((self.N, self.N))
        self.jacobian3 = np.zeros((self.N, self.N))
        self.jacobian4 = np.zeros((self.N, self.N))
        self.jacobian = None    # entire Jacobian with removed buses

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

    def solve_newton_raphson(self):
        # step 1: update the y vector using start data
        for k in range(self.N):
            P, Q = 0, 0

            for n in range(self.N):
                P += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                Q += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])

            self.y[k] -= self.x[k + self.N] * P
            self.y[k + self.N] -= self.x[k + self.N] * Q

        # step 2: solve the jacobian matrix
        self.jacobian = self.solve_jacobian()

    def solve_jacobian(self):
        for k in range(self.N):
            j1, j2, j3, j4 = 0, 0, 0, 0  # summations for the diagonal elements

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

        # remove the slack bus from vectors and jacobian arrays
        self.x = self.remove_slack_bus(self.x)
        self.y = self.remove_slack_bus(self.y)
        self.jacobian1 = self.remove_slack_bus(self.jacobian1)
        self.jacobian2 = self.remove_slack_bus(self.jacobian2)
        self.jacobian3 = self.remove_slack_bus(self.jacobian3)
        self.jacobian4 = self.remove_slack_bus(self.jacobian4)
        self.removed_buses += 1

        # remove the pv bus from jacobian quadrants
        self.jacobian2 = self.remove_pv_bus(7, 2, self.jacobian2)
        self.jacobian3 = self.remove_pv_bus(7, 3, self.jacobian3)
        self.jacobian4 = self.remove_pv_bus(7, 4, self.jacobian4)
        self.removed_buses += 1

        # concatenate the quadrants to form the full jacobian matrix
        jacobian13 = np.concatenate((self.jacobian1, self.jacobian3), axis=0)
        jacobian24 = np.concatenate((self.jacobian2, self.jacobian4), axis=0)
        jacobian = np.concatenate((jacobian13, jacobian24), axis=1)

        return jacobian

    def remove_slack_bus(self, array):
        slack_index = self.slack_bus - 1 - self.removed_buses

        array = np.delete(array, slack_index, axis=0)

        if array.ndim == 2:
            array = np.delete(array, slack_index, axis=1)
        else:   # removing from one of the vectors, they have two slack elements
            array = np.delete(array, slack_index + self.N - 1, axis=0)

        return array

    def remove_pv_bus(self, pv_bus, quadrant, array):
        pv_index = pv_bus - 1 - self.removed_buses

        if quadrant == 2:
            array = np.delete(array, pv_index, axis=1)
        elif quadrant == 3:
            array = np.delete(array, pv_index, axis=0)
        elif quadrant == 4:
            array = np.delete(array, pv_index, axis=0)
            array = np.delete(array, pv_index, axis=1)

        return array



