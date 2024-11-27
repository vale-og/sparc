# SPARC:  Stellar Population Analysis with Remnant Calculations


Monte Carlo simulation for a stellar population with constant star formation and a predefined Initial Mass Function (Kroupa (2001)).

Requires python 3.7 or higher, and the following libraries: matplotlib, pandas, numpy, scipy and time.

To run:
1) Open a terminal inside the SPARC folder, and run:

``` python MAIN.py ```

2) Input the initial star number, to select how many object to simulate, the random seed (just added to be able to reproduce results) and wait for the code to be done! The Main Sequence and evolved stars will be saved in separate .csv files

3) As an extra step, you can chose to create two plots:
a) Mass and age distribution of the Main Sequence stars obtained from the simulation.
b) Final mass and age from the evolved stars, separated into categories according to the obtained remnant.
Both of these plots will be saved as .pdf files in the SPARC/figures/ folder



