# Spectrum_Analyser

This project has been renewed starting from the previous project FTIR_Analisys.
This software is a program that reads some data, Fourier transform them if necessary, then computes the transmission/reflection and plots the outcome (and saves all the results).

There is a certain degree of customization in the plot properties: possibility to add a second comparison set of data (only for the non fft case) and change the units to show in the plot as well as the plot type.
The program can be execurted as a main or from another program.

Although not implemented yet the fitting function provided is built around the lmfit package (http://cars9.uchicago.edu/software/python/lmfit/index.html).

Near future improvements: Normalization, peak finding, peak fitting (functions built not fully tested yet!)

not-so-near future improvements: implementtion of a fit also for the full spectrum (not only for peaks), inizialization from command line
