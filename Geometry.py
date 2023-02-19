import math


class Geometry:
    def __init__(self, x_a, x_b, x_c, y_a, y_b, y_c):
        # x-coordinates of each phase (ft), leftmost is taken to be 0
        self.x_a = x_a
        self.x_b = x_b
        self.x_c = x_c

        # y-coordinates of each phase (ft), above ground
        self.y_a = y_a
        self.y_b = y_b
        self.y_c = y_c

        self.D_ab = None
        self.D_bc = None
        self.D_ca = None
        self.D_eq = None

    def calculate_GMD(self):
        self.D_ab = math.sqrt((self.x_a - self.x_b)**2 + (self.y_a - self.y_b)**2)
        self.D_bc = math.sqrt((self.x_b - self.x_c)**2 + (self.y_b - self.y_c)**2)
        self.D_ca = math.sqrt((self.x_c - self.x_a)**2 + (self.y_c - self.y_a)**2)
        self.D_eq = (self.D_ab * self.D_bc * self.D_ca)**(1 / 3)

        return self.D_eq


geometry = Geometry(0, 19.5, 39, 0, 0, 0)   # all lines at same height, y-coordinates obsolete
print(geometry.calculate_GMD())
