import numpy as np
from math import sin, cos

np.set_printoptions(linewidth=200)


class PowerFlow:
    def __init__(self, system, y_bus):
        # import relevant system data
        self.system = system
        self.slack_bus = 0
        self.pv_bus = 6                 # TODO: check each bus, import to list if PV
        self.N = len(system.buses)      # number of buses in the system (including slack)

        self.Y_bus, self.theta = np.absolute(y_bus), np.angle(y_bus)  # import relevant Ybus data

        self.x, self.y = np.zeros(2 * self.N), np.empty(2 * self.N)     # create empty power flow vectors
        self.jacobian = None

        # TODO: exclude slack bus from the beginning
        # initialize y vector with bus powers
        for k in range(self.N):
            if (k + 1) == self.slack_bus:   # easier to include slack bus and remove later than never include
                self.y[k] = None
                self.y[k + self.N] = None
            else:
                self.y[k] = self.system.buses.get(str(k + 1)).power
                self.y[k + self.N] = self.system.buses.get(str(k + 1)).reactive

        self.y = self.remove_bus(self.y, self.slack_bus)    # y doesn't need the slack bus during power flow iterations
        self.y = self.y / system.S_base                     # change to pu

    def flat_start(self):
        for k in range(self.N):
            self.system.buses.get(str(k + 1)).set_voltage(0, 1.0)
            self.x[k] = self.system.buses.get(str(k + 1)).angle
            self.x[k + self.N] = self.system.buses.get(str(k + 1)).voltage

    def solve_newton_raphson(self):
        # step 1: compute delta y
        delta_y = np.empty_like(self.y)
        N = self.N - 1  # number of buses excepting the slack (for use indexing Q in y vectors)

        for k in range(1, self.N):
            P, Q = 0, 0     # accumulator terms for summations in P_k and Q_k

            for n in range(self.N):
                P += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                Q += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])

            delta_y[k-1] = self.y[k-1] - self.x[k + self.N] * P
            delta_y[k-1 + N] = self.y[k-1 + N] - self.x[k + self.N] * Q

        # step 2: calculate the Jacobian matrix
        jacobian = self.solve_jacobian()

        # step 3: solve for delta_x
        jacobian_inv = np.linalg.inv(jacobian)
        delta_y = np.delete(delta_y, self.pv_bus - 1 + N)   # delete pv bus Q so sizes match for solving
        delta_x = np.dot(jacobian_inv,delta_y)

        # return slack and pv bus values omitted during solving
        delta_x = np.insert(delta_x, [0, self.N - 1], 0)
        delta_x = np.append(delta_x, 0)

        # step 4: compute x for the next iteration
        self.x += delta_x
        print(self.x)
        
    # TODO: automatically exclude slack bus
    def solve_jacobian(self):
        # initialize Jacobian quadrants
        J1, J2, J3, J4 = np.empty((self.N,self.N)), np.empty((self.N,self.N)), np.empty((self.N,self.N)), np.empty((self.N,self.N))

        # solve Jacobian quadrants
        for k in range(self.N):
            sum_j1, sum_j2, sum_j3, sum_j4 = 0, 0, 0, 0     # accumulators for summations in diagonal terms

            for n in range(self.N):
                # inclusive sums
                sum_j2 += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                sum_j4 += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])

                # off-diagonal elements and exclusive sums
                if n != k:
                    sum_j1 += self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])
                    sum_j3 += self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])

                    J1[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * self.x[n + self.N] * sin(self.x[k] - self.x[n] - self.theta[k,n])
                    J2[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                    J3[k,n] = -1 * self.x[k + self.N] * self.Y_bus[k,n] * self.x[n + self.N] * cos(self.x[k] - self.x[n] - self.theta[k,n])
                    J4[k,n] = self.x[k + self.N] * self.Y_bus[k,n] * sin(self.x[k] - self.x[n] - self.theta[k,n])

            # diagonal elements
            J1[k,k] = -1 * self.x[k + self.N] * sum_j1
            J2[k,k] = self.x[k + self.N] * self.Y_bus[k,k] * cos(self.theta[k,k]) + sum_j2
            J3[k,k] = self.x[k + self.N] * sum_j3
            J4[k,k] = -1 * self.x[k + self.N] * self.Y_bus[k,k] * sin(self.theta[k,k]) + sum_j4

        # remove slack bus from quadrants
        J1 = self.remove_bus(J1, self.slack_bus)
        J2 = self.remove_bus(J2, self.slack_bus)
        J3 = self.remove_bus(J3, self.slack_bus)
        J4 = self.remove_bus(J4, self.slack_bus)

        # remove pv bus from quadrants
        J2 = np.delete(J2, self.pv_bus - 1, axis=1)
        J3 = np.delete(J3, self.pv_bus - 1, axis=0)
        J4 = np.delete(J4, self.pv_bus - 1, axis=0)
        J4 = np.delete(J4, self.pv_bus - 1, axis=1)

        # concatenate quadrants to form Jacobian
        J13 = np.concatenate((J1,J3), axis=0)
        J24 = np.concatenate((J2,J4), axis=0)
        jacobian = np.concatenate((J13,J24), axis=1)

        return jacobian

    # TODO: count buses removed
    def remove_bus(self, array, bus):
        if array.ndim == 1:
            array = np.delete(array, bus + self.N, axis=0)
            array = np.delete(array, bus, axis=0)
        elif array.ndim == 2:
            array = np.delete(array, bus, axis=0)
            array = np.delete(array, bus, axis=1)

        return array
