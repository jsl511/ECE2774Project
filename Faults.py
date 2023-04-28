import numpy as np
from math import pi

class Faults:

    #Bus K is the bus of interested
    def __init__(self,system,powerflow,sequence,bus_k):

        self.system=system
        self.powerflow=powerflow
        self.currentArray=np.zeros(1, 3)
        self.v_f=self.powerflow.V*np.exp(1j*self.powerflow.delta)
        self.sequence=sequence
        self.bus_k=bus_k

    #bus is where the fault occurs

    def Symmetrical_fault(self, bus):

        bus=int(bus)-1

        self.currentArray[1]=self.v_f[bus]/self.sequence.z_positive[bus,bus]
        self.currentArray[2]=0
        self.currentArray[0]=0


    def Single_line_to_ground(self, bus,zf):

        bus = int(bus) - 1

        self.currentArray[1] = self.v_f[bus] / (self.sequence.z_positive[bus, bus]+self.sequence.z_negative[bus, bus]+self.sequence.z_zero[bus, bus]+3*zf)
        self.currentArray[2] = self.currentArray[1]
        self.currentArray[0] = self.currentArray[1]

        self.__voltage_and_current_calculations(bus)


    def Line_to_line_fault(self, bus, zf ):

        bus = int(bus) - 1

        self.currentArray[1] = self.v_f[bus] / (self.sequence.z_positive[bus, bus] + self.sequence.z_negative[bus, bus] + self.sequence.z_zero[bus, bus] + zf)
        self.currentArray[2] = -1*self.currentArray[1]
        self.currentArray[0] = 0

        self.__voltage_and_current_calculations(bus)

    def double_line_to_ground(self, bus, zf):


        bus = int(bus) - 1
        self.currentArray[1] = self.v_f[bus] / (self.sequence.z_positive[bus, bus] + (self.sequence.z_negative[bus,bus]*(self.sequence.z_zero[bus,bus]+3*zf)/(self.sequence.z_negative+self.sequence.z_zero+3*zf)))
        self.currentArray[2] = -1 * self.currentArray[1] * ((self.sequence.z_zero+3*zf)/(self.sequence.z_zero+3*zf+self.sequence.z_negative))
        self.currentArray[0] = -1 * self.currentArray[1] * ((self.sequence.z_negative)/(self.sequence.z_zero+3*zf+self.sequence.z_positive))

        self.__voltage_and_current_calculations(bus)

    def __voltage_and_current_calculations(self,bus):

        z_seq=np.array([[self.sequence.z_zero[self.bus_k,bus],0,0],[0,self.sequence.z_positive[self.bus_k,bus],0],[0,0,self.sequence.z_negative[self.bus_k,bus]]])
        v_fault=np.array([[0], [self.v_f], [0]])
        v_seq=v_fault-np.matmul(z_seq, self.currentArray)

        a=np.exp(1j*120*pi/180)

        A=np.array([[1,1,1],[1,a**2,a],[1,a,a**2]])

        v_abc=np.matmul(A,v_seq)
        I_abc=np.matmul(A,self.currentArray)



