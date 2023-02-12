from typing import Dict, List, Optional

from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Bus import Bus


class System:
    def __init__(self, name):
        self.name = name

        self.buses_order: List[str]=list()
        self.buses: Dict[str, Bus] = dict()


        self.transmissionlines: Dict[str, TransmissionLine] = dict()
        self.transformers: Dict[str, Transformer] = dict()

    def __add_bus(self, bus):
        if bus not in self.buses.keys():
            self.buses[bus]=Bus(bus)
            self.buses_order.append(bus)

    def add_transmission_line(self,name, length, bus1Connection, bus2Connection, spacing, numberConductors,x_a, x_b, x_c, y_a, y_b, y_c,diameter, GMR, resistance, ampacity,v):
        self.transmissionlines[name]= TransmissionLine( name, length, bus1Connection, bus2Connection, spacing, numberConductors,x_a, x_b, x_c, y_a, y_b, y_c, diameter, GMR, resistance, ampacity,v)
        self.__add_bus(bus1Connection)
        self.__add_bus(bus2Connection)

        self.buses[bus1Connection].setVoltage(v)
        self.buses[bus2Connection].setVoltage(v)

    def add_tranformer(self,name, powerRating, voltageRatingHigh, voltageRatingLow, impedance, xR, bus1Connection, bus2Connection):

        self.transformers[name]= Transformer(name, powerRating, voltageRatingHigh, voltageRatingLow, impedance, xR, bus1Connection, bus2Connection)
        self.__add_bus(bus1Connection)
        self.__add_bus(bus2Connection)


        #TX1.Bundle.setConductor("conductor", 2, 2, 2, 2)
        ##TX1.Bundle.setGeometry(x_a, x_b, x_c, y_a, y_b, y_c)
        ##TX1.Bundle.solveCapacitance()
        ##TX1.Bundle.solveInductance()
        ##TX1.solveImpedance()
        ##TX1.solveShuntAdmittance()


