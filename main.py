from System import System
from Ybus import Ybus
from PowerFlow import PowerFlow
from Sequence import Sequence


# create the 6-node looped transmission system
system = System(100)

system.set_conductor("partridge", 0.642, 0.0217, 460, 0.350)
system.set_bundle("bundle", 1.5, 2)
system.set_geometry(0, 19.5, 39, 0, 0, 0)   # all lines at same height, y-coordinates obsolete

system.add_transformer("T1", 125, 20, 230, 0.085, 10, "1", "2")
system.add_transformer("T2", 200, 20, 230, 0.105, 12, "6", "7")

system.add_line("L1", 10, "2", "4", system.bundle, system.geometry)
system.add_line("L2", 25, "2", "3", system.bundle, system.geometry)
system.add_line("L3", 20, "3", "5", system.bundle, system.geometry)
system.add_line("L4", 20, "4", "6", system.bundle, system.geometry)
system.add_line("L5", 10, "5", "6", system.bundle, system.geometry)
system.add_line("L6", 35, "4", "5", system.bundle, system.geometry)

y_bus = Ybus(system)

system.buses.get("1").set_voltage(0, 1.0)
system.buses.get("2").set_power(0, 0, 0, 0)
system.buses.get("3").set_power(0, 0, 110, 50)
system.buses.get("4").set_power(0, 0, 100, 70)
system.buses.get("5").set_power(0, 0, 100, 65)
system.buses.get("6").set_power(0, 0, 0, 0)
system.buses.get("7").set_power(200, 0, 0, 0)

power_flow = PowerFlow(system, y_bus.y_bus)
power_flow.flat_start()
# power_flow.test_voltage()
power_flow.solve_newton_raphson(0.0001, 10)

system.add_generator("G1", "1", 0, 0.12, 0.14, 0.05)
system.add_generator("G2", "7", 0, 0.12, 0.14, 0.05)

sequence = Sequence(system)
