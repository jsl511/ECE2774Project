import numpy as np
from math import sin, cos
np.set_printoptions(linewidth=200)

# TODO: slack bus other than 1


class PowerFlow:
    def __init__(self, system, y_bus):
        # import relevant system and Ybus data
        self.buses = system.buses
        self.N = len(self.buses)
        self.Y_bus, self.theta = np.absolute(y_bus), np.angle(y_bus)
        # print("Y_bus is: \n" + str(np.around(self.Y_bus, decimals=2)))
        # print("theta is: \n" + str(np.around(self.theta, decimals=2)))

        # initialize power flow vectors and matrices
        self.x = None
        self.delta, self.V = np.zeros(self.N), np.zeros(self.N)     # voltage angles and magnitudes
        self.y = self.__initialize_y()/system.S_base
        self.J = np.zeros((len(self.y), len(self.y)))

    def solve_newton_raphson(self):
        # print("Power vector is: " + str(self.y))
        print("Voltage vector is: " + str(self.delta))
        delta_y = self.__calculate_power_mismatch()     # step 1
        print("Power mismatches are: " + str(np.around(delta_y * 100, decimals=2)))
        # self.J = self.__compute_jacobian()              # step 2

        # J_inv = np.linalg.inv(self.J)
        # delta_y = np.delete(delta_y, 11)    # delete pv bus Q so sizes match for solving
        # delta_x = np.dot(J_inv, delta_y)

        # return slack and pv bus values omitted during solving
        # delta_x = np.insert(delta_x, [0, self.N - 1], 0)
        # delta_x = np.append(delta_x, 0)
        # delta_y = np.append(delta_y, 0)

        # self.x += delta_x
        # print(self.x)

        # self.delta = self.x[:self.N]
        # self.V = self.x[self.N:]
        # delta_y = self.__calculate_power_mismatch()
        # print(delta_y)

    def flat_start(self):
        for k in range(self.N):
            self.delta[k] = 0
            self.V[k] = 1.0
            self.buses.get(str(k+1)).set_voltage(self.delta[k], self.V[k])

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

        for k in range(self.N):
            for n in range(self.N):
                P_x[k-1] += self.V[k] * self.Y_bus[k,n] * self.V[n] * cos(self.delta[k] - self.delta[n] - self.theta[k,n])
                print("k = " + str(k) + " n = " + str(n) + ": Q(x) = " + str(self.V[k] * self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])))
                Q_x[k-1] += self.V[k] * self.Y_bus[k,n] * self.V[n] * sin(self.delta[k] - self.delta[n] - self.theta[k,n])
                # print("k = " + str(k) + " n = " + str(n) + ": Q(x) = " + str(Q_x[k-1]))
        f_x = np.concatenate((P_x,Q_x), axis=0)

        return self.y - f_x   # TODO: why does addition yield the correct result

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

    def __remove_slack_bus(self, array):
        array = np.delete(array, 0, axis=0)
        array = np.delete(array, 0, axis=1)

        return array
