import numpy as np
from math import sin, cos
np.set_printoptions(linewidth=200)


class PowerFlow:
    def __init__(self, system, y_bus):
        # import relevant system and Ybus data
        self.buses = system.buses
        self.N = len(self.buses)
        self.Y_bus, self.theta = np.absolute(y_bus), np.angle(y_bus)

        self.x = None
        self.y = self.__initialize_y()/system.S_base
        self.J = np.empty((len(self.y), len(self.y)))

    def solve_newton_raphson(self):
        delta_y = self.__calculate_power_mismatch()
        print(delta_y)

    def flat_start(self):
        delta, V = np.empty(self.N), np.empty(self.N)

        for k in range(self.N):
            delta[k] = 0
            V[k] = 1.0
            self.buses.get(str(k+1)).set_voltage(delta[k], V[k])

        self.x = np.concatenate((delta, V), axis=0)

    # initializes the y-vector using the given bus powers
    def __initialize_y(self):
        P, Q = np.empty(self.N - 1), np.empty(self.N - 1)

        for k in range(1,self.N):
            P[k-1] = self.buses.get(str(k+1)).power
            Q[k-1] = self.buses.get(str(k+1)).reactive

        return np.concatenate((P,Q), axis=0)

    def __calculate_power_mismatch(self):
        P_x, Q_x = np.zeros(self.N - 1), np.zeros(self.N - 1)
        delta, V = self.x[:self.N], self.x[self.N:]

        for k in range(1,self.N):
            for n in range(self.N):
                P_x[k-1] += V[k] * self.Y_bus[k,n] * V[n] * cos(delta[k] - delta[n] - self.theta[k,n])
                Q_x[k-1] += V[k] * self.Y_bus[k,n] * V[n] * sin(delta[k] - delta[n] - self.theta[k,n])

        y = np.concatenate((P_x,Q_x), axis=0)
        return self.y + y

    def __compute_jacobian(self):
        pass
