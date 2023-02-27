from System import System
from Ybus import Ybus

# create the 6-node looped transmission system
system = System()

system.set_conductor("partridge", 0.642, 0.0217, 460, 0.350)
system.set_bundle("bundle", 1.5, 2)
system.bundle.calculate_GMR()
system.set_geometry(0, 19.5, 39, 0, 0, 0)   # all lines at same height, y-coordinates obsolete
system.geometry.calculate_GMD()

system.add_transformer("T1", 125, 20, 230, 0.085, 10, "1", "2")
system.add_transformer("T2", 200, 20, 230, 0.105, 12, "6", "7")

system.add_line("L1", 10, "2", "4", system.bundle, system.geometry)
system.add_line("L2", 25, "2", "3", system.bundle, system.geometry)
system.add_line("L3", 20, "3", "5", system.bundle, system.geometry)
system.add_line("L4", 20, "4", "6", system.bundle, system.geometry)
system.add_line("L5", 10, "6", "5", system.bundle, system.geometry)
system.add_line("L6", 35, "4", "5", system.bundle, system.geometry)

y_bus = Ybus()
y_bus.calculate_Ybus(system)
