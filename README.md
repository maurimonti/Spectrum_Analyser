# FTIR_Analysis

This project is meant to be a software that reads and analyse the data from an FTIR spectrometer, however can be also used to read and plot data from any source (if the correct formatting is provided).
At the moment only the plotting function of the reflectivity and trnasmittivity are present.

The script reads data from a csv or a standard tab/space file, divides the signal and a comparison set of data for a reference and plot the result as a function of the wavelength. There is the option to provide a background measurement to subtract both for the signal and the reference.

The script can be used inserting the asked parameters (file positions, figure properties...) and making it run as main.

Near-future improvements: allow change of the x axis from the preamble.

Not-so-near-future improvements: allow variables initialization from the command line, insert different plotting possibility (ex. plotting also the non-normalized data)
