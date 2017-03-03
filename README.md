# FTIR_Analysis

This project is meant to be a software that reads and analyse the data from an FTIR spectrometer, however can be also used to read and plot data from any source (if the correct formatting is provided).

The script reads data from a csv or a standard tab/space file, divides the signal and a comparison set of data for a reference and plot the result as a function of the wavelength. There is the option to provide a background measurement to subtract both for the signal and the reference.
The script is now divided into two files: one for the main and variable inizialization and another one for the functions.
All the functions are now self-sustaining: everything is more flexible and definetly more ordered.
Added the possibilities to change the x unit and the plot type.

The script can be used inserting the asked parameters (file positions, figure properties...) and making it run as main.

Near-future improvements: Normalization of the data (function built, testing and implementation not yet) Peak Fitting.

Not-so-near-future improvements: allow variables initialization from the command line, insert different plotting possibility (ex. plotting also the non-normalized data)
