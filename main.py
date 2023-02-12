# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settin

from System import System

testSystem=System("test")

testSystem.add_tranformer("transformer1", 100, 140, 110, 2, 10, "A", "B")
testSystem.add_transmission_line("line1", 5, "B", "C", 2, 3,5, 4, 3, 3, 2, 1,3, 3, 2, 1,120)

