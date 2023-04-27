from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry
from Bus import Bus
from TransmissionLine import TransmissionLine
from Transformer import Transformer
from Generator import Generator


class System:
    def __init__(self, S_base):
        # assumes one conductor, geometry, and bundling configuration for the entire system
        # to accommodate multiples, change to str:Obj dictionaries; methods to add_<element>()
        self.conductor = None
        self.bundle = None
        self.geometry = None

        # empty dictionaries to hold elements with string keys and Object values
        self.buses = {}
        self.generators = {}
        self.lines = {}
        self.transformers = {}

        # MVA base for entire system and empty lists to hold V and Z bases for different regions
        self.S_base = S_base
        self.V_bases = []
        self.Z_bases = []

    def __add_bus(self, name):
        if name not in self.buses.keys():
            self.buses.update({name: Bus(name)})

    def add_generator(self, name, bus, power, positive_impedance, negative_impedance, zero_impedance):
        if name not in self.generators.keys():
            self.generators.update({name: Generator(name, bus, power, positive_impedance, negative_impedance, zero_impedance)})
            self.__add_bus(bus)
            # TODO: set bus power based on generator power
            
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

            if voltage1 not in self.V_bases:
                self.__add_base(voltage1)

            if voltage2 not in self.V_bases:
                self.__add_base(voltage2)

    def set_conductor(self, name, diameter, GMR, ampacity, resistance):
        self.conductor = Conductor(name, diameter, GMR, ampacity, resistance)

    def set_bundle(self, name, spacing, number_conductors):
        self.bundle = Bundle(name, spacing, number_conductors, self.conductor)

    def set_geometry(self, x_a, x_b, x_c, y_a, y_b, y_c):
        self.geometry = Geometry(x_a, x_b, x_c, y_a, y_b, y_c)

    def __add_base(self, V_base):
        self.V_bases.append(V_base)
        # I_base = self.S_base/V_base     # check for LL or LG voltage
        Z_base = (V_base * V_base)/self.S_base  # assumes LL
        self.Z_bases.append(Z_base)

        # regions are determined by index of lists
            # how to track current region? by bus?
