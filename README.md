# ECE 2774 Advanced Power Systems Analysis

## Milestone 1: Develop Power Flow System Ybus Matrix
The code written for this milestone is composed of all files in the repository as of 03/01/2022

### System Definition Methods
* Bundle.py - allows the user to create a bundling configuration of lines
* Bus.py - creates a new bus in the system (the user cannot do this directly)
* Conductor.py - allows the user to create a conductor used in the lines
* Geometry.py - allows the user to create a spatial configuration of lines
* System.py - builds the assigned system using a single bundle, conductor, and geometry 

### Transformer.py
Creates a new transformer object given the nameplate ratings and connected buses. New buses will be created using Bus.py. Admittance is calculated via a class method.

### TransmissionLine.py
Creates a new transmission line object given the length, a bundle, a geometry, and connected buses. New buses will be created using Bus.py. Capacitance, inductance, impedance, and admittance are calculated via class methods.

### Ybus.py
Creates the system's Ybus matrix as a complex array using numpy. Two for-loops (one for the transformers and one for the transmission lines) iterate through each system element and modify the admittance at and between its connected buses accordingly.
