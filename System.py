from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry
from Bus import Bus
from TransmissionLine import TransmissionLine
from Transformer import Transformer
import numpy as np
import math

class System:

    def __init__(self):
        # assumes one conductor, geometry, and bundling configuration for the entire system
        # to accommodate multiples, change to str:Obj dictionaries; methods to add_<element>()
        self.conductor = None
        self.bundle = None
        self.geometry = None

        # empty dictionaries to hold elements with string keys and Object values
        self.buses = {}
        self.lines = {}
        self.transformers = {}

        #creating empty jacobian matrix
        self.jacobian1 = None
        self.jacobian2 = None
        self.jacobian3 = None
        self.jacobian4 = None

    def __add_bus(self, name):
        if name not in self.buses.keys():
            self.buses.update({name: Bus(name)})

    def add_line(self, name, length, bus1, bus2, bundle, geometry):
        if name not in self.lines.keys():
            self.lines.update({name: TransmissionLine(name, length, bus1, bus2, bundle, geometry)})
            self.lines.get(name).calculate_capacitance()
            self.lines.get(name).calculate_inductance()
            self.lines.get(name).calculate_impedance()
            self.lines.get(name).calculate_admittance()
            self.__add_bus(bus1)
            self.__add_bus(bus2)

    def add_transformer(self, name, power, voltage1, voltage2, impedance, x_r, bus1, bus2):
        if name not in self.transformers.keys():
            self.transformers.update(({name: Transformer(name, power, voltage1, voltage2, impedance, x_r, bus1, bus2)}))
            self.transformers.get(name).calculate_admittance()
            self.__add_bus(bus1)
            self.__add_bus(bus2)

    def set_conductor(self, name, diameter, GMR, ampacity, resistance):
        self.conductor = Conductor(name, diameter, GMR, ampacity, resistance)

    def set_bundle(self, name, spacing, number_conductors):
        self.bundle = Bundle(name, spacing, number_conductors, self.conductor)

    def set_geometry(self, x_a, x_b, x_c, y_a, y_b, y_c):
        self.geometry = Geometry(x_a, x_b, x_c, y_a, y_b, y_c)


    def solve_jacobian(self,Ybus):
        #4 arrays and concatenate?
        j1tot = 0
        j2tot = 0
        j3tot = 0
        j4tot = 0
        self.jacobian1=np.zeros((len(self.buses), len(self.buses)))
        self.jacobian2= np.zeros((len(self.buses), len(self.buses)))
        self.jacobian3= np.zeros((len(self.buses), len(self.buses)))
        self.jacobian4= np.zeros((len(self.buses), len(self.buses)))

        #summing totals
        for k in self.buses:
            for n in self.buses:
                kint = int(k) - 1
                nint = int(n) - 1
                # computation for none diagonal elements
                if n != k:
                    j1tot = j1tot + abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.sin(self.buses.get(k).angle - self.buses.get(n).angle - np.angle(Ybus.y_bus[kint, nint]))
                    j3tot = j3tot + abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.cos(self.buses.get(k).angle - self.buses.get(n).angle - np.angle(Ybus.y_bus[kint, nint]))
                j2tot = j2tot + abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.cos(self.buses.get(k).angle - self.buses.get(n).angle - np.angle(Ybus.y_bus[kint, nint]))
                j4tot = j4tot + abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.sin(self.buses.get(k).angle - self.buses.get(n).angle - np.angle(Ybus.y_bus[kint, nint]))


        for k in self.buses:
            for n in self.buses:
                kint = int(k)-1
                nint = int(n)-1

                if n != k:
                    #off-diagonal elements of J
                    self.jacobian1[kint, nint] = self.buses.get(k).voltage * abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.sin(self.buses.get(k).angle-self.buses.get(n).angle-np.angle(Ybus.y_bus[kint, nint]))
                    self.jacobian2[kint, nint] = self.buses.get(k).voltage * abs(Ybus.y_bus[kint, nint]) * math.cos(self.buses.get(k).angle-self.buses.get(n).angle-np.angle(Ybus.y_bus[kint, nint]))
                    self.jacobian3[kint, nint] = -self.buses.get(k).voltage * abs(Ybus.y_bus[kint, nint]) * self.buses.get(n).voltage * math.cos(self.buses.get(k).angle-self.buses.get(n).angle-np.angle(Ybus.y_bus[kint, nint]))
                    self.jacobian4[kint, nint] = self.buses.get(k).voltage * abs(Ybus.y_bus[kint, nint]) * math.sin(self.buses.get(k).angle-self.buses.get(n).angle-np.angle(Ybus.y_bus[kint, nint]))
                if n == k:
                    #diagonal elements
                    self.jacobian1[kint, nint] = -self.buses.get(k).voltage*j1tot
                    self.jacobian2[kint, nint] = self.buses.get(k).voltage*abs(Ybus.y_bus[kint, nint])*math.cos(np.angle(Ybus.y_bus[kint, nint]))+j2tot
                    self.jacobian3[kint, nint] = self.buses.get(k).voltage*j3tot
                    self.jacobian4[kint, nint] = -self.buses.get(k).voltage*abs(Ybus.y_bus[kint, nint])*math.sin(np.angle(Ybus.y_bus[kint, nint]))+j4tot

        #concatenating arrays

        jacobian13 = np.concatenate((self.jacobian1, self.jacobian3), axis=0)
        jacobian24 = np.concatenate((self.jacobian2, self.jacobian4), axis=0)
        jacobian= np.concatenate((jacobian13, jacobian24), axis=1)

        print(np.around(jacobian, decimals=1))


    def flat_start(self):
        for value in self.buses.values():
            value.set_voltage(1, 0)







