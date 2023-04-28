import numpy as np

class Faults:

    def __init__(self,system):

        self.system=system


    def Symmetrical_fault(self, bus1):
        #convertBus1toNumber

        #I(+)atBusN=VF(PreFault_Voltage)/(Z(+)atBusNN
        #I(-)atBusN=0
        #I(0)atBusN=0

    def Single_line_to_ground(self, bus1,line1):

        # convertBus1toNumber
        # convertLine1toNumber

        # I(+)atBusN=VF(PreFault_Voltage)/(Z(+)atBusNN+Z(-)atBusNN+Z(0)atBusNN+3ZF)
        # I(-)atBusN= I(+)
        # I(0)atBusN= I(+)
    def Line_to_line_fault(self, bus1,line1,line2 ):

        # convertBus1toNumber
        # convertLine1toNumber
        # convertLne2toNumber

        # I(+)atBusN=VF(PreFault_Voltage)/(Z(+)atBusNN+Z(-)atBusNN+Z(0)atBusNN+ZF)
        # I(-)atBusN= -1*I(+)
        # I(0)atBusN= 0
    def double_line_to_ground(self, bus1, line1,line2):

        # convertBus1toNumber
        # convertLine1toNumber
        # convertLne2toNumber

        #Yeah no you are gonna get confused if i pseudo code this
    def __voltage_and_current_calculations(self):
        #im 1/2 lost here.


