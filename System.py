from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry
from Bus import Bus
from TransmissionLine import TransmissionLine
from Transformer import Transformer


class System:
    def __init__(self):
        # assumes one conductor, geometry, and bundling configuration for the entire system
        self.conductor = None
        self.bundle = None
        self.geometry = None

        self.buses = {}
        self.lines = {}
        self.transformers = {}

    def __add_bus(self, name):
        if name not in self.buses.keys():
            self.buses.update({name: Bus(name)})

    def add_line(self, name, length, bus1, bus2, bundle, geometry):
        if name not in self.lines.keys():
            self.lines.update({name: TransmissionLine(name, length, bus1, bus2, bundle, geometry)})
            self.__add_bus(bus1)
            self.__add_bus(bus2)

    def add_transformer(self, name, power, voltage1, voltage2, impedance, x_r, bus1, bus2):
        if name not in self.transformers.keys():
            self.transformers.update(({name: Transformer(name, power, voltage1, voltage2, impedance, x_r, bus1, bus2)}))
            self.__add_bus(bus1)
            self.__add_bus(bus2)

    def set_conductor(self, name, diameter, GMR, ampacity, resistance):
        self.conductor = Conductor(name, diameter, GMR, ampacity, resistance)

    def set_bundle(self, name, spacing, number_conductors):
        self.bundle = Bundle(name, spacing, number_conductors, self.conductor)

    def set_geometry(self, x_a, x_b, x_c, y_a, y_b, y_c):
        self.geometry = Geometry(x_a, x_b, x_c, y_a, y_b, y_c)
