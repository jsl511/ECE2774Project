# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settin

from System import System

testSystem=System("test")

testSystem.add_tranformer("transformer1", 100, 140, 110, 2, 10, "A", "B")
conductor=testSystem.add_conductor("conductor1",3,3,3,3)
geometry=testSystem.add_geometry(3,4,5,1,2,3)
testSystem.add_transmission_line("line1", 5, "B", "C", 2, 3,geometry,conductor,120)

