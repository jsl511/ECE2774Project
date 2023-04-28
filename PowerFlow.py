import math

import numpy as np
from math import sin, cos, pi
np.set_printoptions(linewidth=200)

# TODO: slack bus other than 1


class PowerFlow:
    def __init__(self, system, y_bus):
        # import relevant system and Ybus data
        self.buses = system.buses
        self.N = len(self.buses)
        self.Y_bus, self.theta = np.absolute(y_bus), np.angle(y_bus)

        # initialize power flow vectors and matrices
        self.x = None
        self.delta, self.V = np.zeros(self.N), np.zeros(self.N)     # voltage angles and magnitudes
        self.y = self.__initialize_y()/system.S_base
        self.J = None

    def solve_newton_raphson(self, tolerance, max_its):
        converged = False
        iterations = 0  # number of iterations completed

        while not converged:
            delta_y = self.__calculate_power_mismatch()     # step 1

            # check for convergence
            if np.all(delta_y < tolerance):
                converged = True
                self.__print_solutions(iterations)
            else:
                self.J = self.__compute_jacobian()          # step 2

                J_inv = np.linalg.inv(self.J)
                delta_y = np.delete(delta_y, 11)  # delete pv bus Q so sizes match for solving
                delta_x = np.dot(J_inv, delta_y)            # step 3

                # return slack and pv bus values omitted during solving
                delta_x = np.insert(delta_x, [0, self.N - 1], 0)
                delta_x = np.append(delta_x, 0)
                delta_y = np.append(delta_y, 0)

                self.x += delta_x                           # step 4

                # assign new voltage data for next iteration
                self.delta = self.x[:self.N]
                self.V = self.x[self.N:]

                iterations += 1     # completed one iteration

                # check for max iterations
                if iterations > max_its:
                    print("Solution diverged")
                    exit(1)

    def flat_start(self):
        for k in range(self.N):
            self.delta[k] = 0
            self.V[k] = 1.0
            self.buses.get(str(k+1)).set_voltage(self.delta[k], self.V[k])

        self.x = np.concatenate((self.delta, self.V), axis=0)

    def test_voltage(self):
        self.delta = [0.00, -5.84, -6.97, -6.11, -6.23, -5.21, 7.80]
        self.V = [1, 0.88877, 0.86935, 0.87897, 0.87372, 0.88557, 1]

        for k in range(len(self.delta)):
            self.delta[k] = self.delta[k] * (pi/180)

        self.x = np.concatenate((self.delta, self.V), axis=0)

    # initializes the y-vector using the given bus powers
    def __initialize_y(self):
        P, Q = np.zeros(self.N - 1), np.zeros(self.N - 1)

        for k in range(1,self.N):
            P[k-1] = self.buses.get(str(k+1)).power
            Q[k-1] = self.buses.get(str(k+1)).reactive

        return np.concatenate((P,Q), axis=0)

    def __calculate_power_mismatch(self):
        P_x, Q_x = np.zeros(self.N - 1), np.zeros(self.N - 1)

        for k in range(1,self.N):
            for n in range(self.N):
                P_x[k-1] += self.V[k] * self.Y_bus[k,n] * self.V[n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])
                Q_x[k-1] += self.V[k] * self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])

        f_x = np.concatenate((P_x,Q_x), axis=0)

        return self.y - f_x

    def __compute_jacobian(self):
        # Jacobian quadrants
        J1, J2, J3, J4 = np.zeros((self.N,self.N)), np.zeros((self.N,self.N)), np.zeros((self.N,self.N)), np.zeros((self.N,self.N))

        for k in range(self.N):
            J2[k,k] += self.V[k] * self.Y_bus[k,k] * cos(self.theta[k,k])
            J4[k,k] += -1 * self.V[k] * self.Y_bus[k,k] * sin(self.theta[k,k])

            for n in range(self.N):
                J2[k,k] += self.Y_bus[k,n] * self.V[n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])
                J4[k,k] += self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])

                if n != k:
                    J1[k,k] += -1 * self.V[k] * self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])
                    J3[k,k] += self.V[k] * self.Y_bus[k,n] * self.V[n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])

                    J1[k,n] = self.V[k] * self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])
                    J2[k,n] = self.V[k] * self.Y_bus[k,n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])
                    J3[k,n] = -1 * self.V[k] * self.Y_bus[k,n] * self.V[n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])
                    J4[k,n] = self.V[k] * self.Y_bus[k,n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])

        # remove slack bus from quadrants
        J1 = self.__remove_slack_bus(J1)
        J2 = self.__remove_slack_bus(J2)
        J3 = self.__remove_slack_bus(J3)
        J4 = self.__remove_slack_bus(J4)

        # remove pv bus from quadrants
        J2 = np.delete(J2, 5, axis=1)
        J3 = np.delete(J3, 5, axis=0)
        J4 = np.delete(J4, 5, axis=0)
        J4 = np.delete(J4, 5, axis=1)

        # concatenate quadrants to form Jacobian
        J13 = np.concatenate((J1, J3), axis=0)
        J24 = np.concatenate((J2, J4), axis=0)
        jacobian = np.concatenate((J13, J24), axis=1)

        return jacobian

    @staticmethod
    def __remove_slack_bus(array):
        array = np.delete(array, 0, axis=0)
        array = np.delete(array, 0, axis=1)

        return array

    def __print_solutions(self, iterations):
        print("Solution converged in " + str(iterations) + " iterations. \n")
