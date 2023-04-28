import numpy as np

class Faults:

    def __init__(self,system,powerflow,sequence):

        self.system=system
        self.powerflow=powerflow
        self.currentArray=np.zeros(1, 3)
        self.v_f=self.powerflow.V*np.exp(1j*self.powerflow.delta)
        self.sequence=sequence
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

    def Line_to_line_fault(self, bus, zf ):

        bus = int(bus) - 1

        self.currentArray[1] = self.v_f[bus] / (self.sequence.z_positive[bus, bus] + self.sequence.z_negative[bus, bus] + self.sequence.z_zero[bus, bus] + zf)
        self.currentArray[2] = -1*self.currentArray[1]
        self.currentArray[0] = 0

    def double_line_to_ground(self, bus, zf):


        bus = int(bus) - 1
        self.currentArray[1] = self.v_f[bus] / (self.sequence.z_positive[bus, bus] + (self.sequence.z_negative[bus,bus]*(self.sequence.z_zero[bus,bus]+3*zf)/(self.sequence.z_negative+self.sequence.z_zero+3*zf)))
        self.currentArray[2] = -1 * self.currentArray[1] * ((self.sequence.z_zero+3*zf)/(self.sequence.z_zero+3*zf+self.sequence.z_negative))
        self.currentArray[0] = -1 * self.currentArray[1] * ((self.sequence.z_negative)/(self.sequence.z_zero+3*zf+self.sequence.z_positive))


    def __voltage_and_current_calculations(self):
        
        pass


