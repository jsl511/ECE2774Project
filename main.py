from System import System

# create the 6-node looped transmission system
system = System()

system.set_conductor("partridge", 0.642, 0.0217, 460, 0.350)
system.set_bundle("bundle", 1.5, 2)
system.bundle.calculate_GMR()
system.set_geometry(0, 19.5, 39, 0, 0, 0)   # all lines at same height, y-coordinates obsolete
system.geometry.calculate_GMD()

system.add_transformer("T1", 125, 20, 230, 0.085, 10, "1", "2")
system.add_transformer("T2", 200, 20, 230)
system.add_line("L1", 10, "2", "4", system.bundle, system.geometry)
