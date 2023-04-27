# ECE 2774 Advanced Power Systems Analysis

## Milestone 1: Develop Power Flow System Ybus Matrix
The code written for this milestone is composed of all files in the repository as of 04/27/2022

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

## Milestone 2: Produce Power Flow Input Data, Jacobian and Injection Equations
The code written for this milestone is composed of all files in the repository as of 04/27/2022

### PowerFlow.py
This class includes all 4 steps required to solve power flow. There is a flat start function which is used one time in the main file. There is then an overarching function called "Solve_newton_raphson" which steps through the 4 parts of power flow. It calculates the power mismatches, solves for the jacobian and then calculates the new "X" value.

## Milestone 3: Solve Power System Power Flow
The code written for this milestone is composed of all files in the repository as of 04/27/2022

### PowerFlow.py
Updated the "Solve_newton_raphson". Updated the function so it runs until the system converges to a solution.



## Milestone 5: Sequence Networks

### XXXX.py
This class solves for the positive, negative and zero sequence networks.













