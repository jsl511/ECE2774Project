from math import sqrt


class Bundle:
    def __init__(self, name, spacing, number_conductors, conductor):
        self.name = name
        self.spacing = spacing  # distance between subconductors (ft)
        self.number_conductors = number_conductors  # number of subconductors in the bundle

        self.conductor = conductor    # Conductor object

        self.resistance = self.conductor.resistance/self.number_conductors   # adjust bundle resistance

        if self.number_conductors == 1:
            self.D_SL = self.conductor.GMR
            self.D_SC = self.conductor.radius
        elif self.number_conductors == 2:
            self.D_SL = sqrt(self.conductor.GMR * self.spacing)
            self.D_SC = sqrt(self.conductor.radius * self.spacing)
        elif self.number_conductors == 3:
            self.D_SL = (self.conductor.GMR * (self.spacing ** 2)) ** (1/3)
            self.D_SC = (self.conductor.radius * (self.spacing ** 2)) ** (1/3)
        elif self.number_conductors == 4:
            self.D_SL = 1.0941 * (self.conductor.GMR * (self.spacing ** 3)) ** (1/4)
            self.D_SC = 1.0941 * (self.conductor.radius * (self.spacing ** 3)) ** (1/4)
        else:
            print("Unexpected number of conductors: greater than 4.")
            exit(1)
