class Conductor:
    def __init__(self, name, diameter, GMR, resistance, ampacity):
        self.name = name
        self.diameter = diameter
        self.radius = self.diameter/2
        self.GMR = GMR
        self.resistance = resistance
        self.ampacity = ampacity
        