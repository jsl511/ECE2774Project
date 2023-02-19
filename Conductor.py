class Conductor:
    def __init__(self, name, diameter, GMR, ampacity, resistance):
        self.name = name
        self.diameter = diameter    # outside diameter (in)
        self.GMR = GMR  # at 60 Hz (ft)
        self.ampacity = ampacity    # (A)
        self.resistance = resistance    # at 25 C (Ohm/mile)

        self.radius = self.diameter / 2


# instantiate a partridge conductor
partridge = Conductor("partridge", 0.642, 0.0217, 460, 0.350)
