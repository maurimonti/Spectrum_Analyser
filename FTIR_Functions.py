# Script containing all the functions needed for the FTIR_Analysis script
# for now it just reds file, compute the spectrum, converts it and plots the
# data. Working on implementing also a peak finding or peak fitting

# Modules
import csv  # read csv easily
import sys  # system methods, used for exit
import numpy as np
import matplotlib.pyplot as plt  # plotting
import scipy.signal as sig  # library with signal analysis (find peaks, etc.)
import scipy.optimize as opt  # contains fitting and minimization tools


def Converter(xIn, yIn, xUnit='cm1', yUnit):
    # This function converts the x in a chosen unit that depends on the xUnit
    # value. At the moment the implementation of the y unit choice is not
    # implemented.
    # Returns the converted data

    if xUnit is 'micro':
        xOut = [x**(-1) * 10000 for x in xIn]

    elif xUnit is 'nm':
        xOut = [x**(-1) * 10000000 for x in xIn]

    elif xUnit is 'eV':
        xOut = [x * 1.23984 * 0.0001 for x in xIn]

    elif xUnit is 'cm1':
        xOut = [x for x in xIn]

    else:
        sys.exit('damn! Unit of measure not recognized or not implemented!')

    yOut = [y * 100 for y in yIn]
    out = np.array([xOut, yOut])

    return out


def Opener(pathFile, sep='tab'):
    # this function open the file and put the data into a list

    dati = []
    if sep is 'csv':
        with open(pathFile) as f:
            dati = list(csv.reader(f))

    elif sep is 'tab' or 'space':
        with open(pathFile, 'r') as f:
            for line in f:
                line = line.strip()
                columns = line.split()
                dati.append(columns)

    return dati


def ReadFTIR(pathFile, sep='tab'):
    # This function reads the file of the FTIR and return them in an array

    numeri = []
    inten = []

    try:
        dati = Opener(pathFile, sep)
        for x in dati:
            for y in x:
                if x.index(y) == 0:
                    numeri.append(float(y))
                if x.index(y) == 1:
                    inten.append(float(y))

    except:
        sys.exit('damn! file type not recognized!')

    data = np.array([numeri, inten])

    return data


def Computer(data, dataRef, dataBack, dataBackRef, Back=0):
    # This function computes the reflectivity spectrum dividing the raw data
    # for a given reference. If Back is True also subtract a given background
    # to compensate for a non good alignment or for a non good aperture size.
    # Returns the wavenumber and the spectrum

    ratio = []
    if Back is True:
        spectrum = data[1] - dataBack[1]
        spectrumRef = dataRef[1] - dataBackRef[1]

    elif Back is False:
        spectrum = data[1]
        spectrumRef = dataRef[1]

    ratio = spectrum / spectrumRef
    return data[0], ratio


def plotter(wavelength, spectrum, shape, name, flag='normal'):
    # This function plots the data, depending on the value of flag changes
    # the plot type.
    # Returns the plot

    if flag is 'normal':
        figure = plt.plot(wavelength, spectrum, shape, label=name)
    elif flag is 'logx':
        figure = plt.semilogx(wavelength, spectrum, shape, label=name)
    elif flag is 'logy':
        figure = plt.semilogy(wavelength, spectrum, shape, label=name)
    elif flag is 'loglog':
        figure = plt.loglog(wavelength, spectrum, shape, label=name)
    else:
        sys.exit('damn! plot type non recognized!')

    return figure


def Normalizer(spectrum, default=0, noisy=False, theoMax=101):
    # Normalization of the data, to a default value called default. If 0 the
    # data will be divided for the maximum. Another parameter noisy can be
    # called if the data are not smooth and deletes all the values that are
    # above a theoretical maximum theoMax.
    # It returns the normalized spectrum

    if default is 0:
        if noisy is False:
            maxVal = np.nanmax(spectrum)
            out = spectrum / maxVal
            return out

        elif noisy is True:
            maximaVal = spectrum[sig.argrelmax(spectrum)]
            maximaVal = maximaVal[np.where(maximaVal < theoMax)]
            maxVal = np.nanmax(maximaVal)
            out = spectrum / maxVal
            return out

        else:
            sys.exit('WTF? I don\'t know how the noise is!')

    elif default < 0:
        sys.exit('Damn! Normalization value is negative!')

    else:
        out = spectrum / default
        return out


def FindPeaks(freq, spectrum, widths, Top=101):
    # Uses find_peaks_cwt of the Scipy.signal library to find peaks, then
    # returns the peak positions and heights. Top is needed to delete all the
    # Nonphysical peaks that are above the maximum possible value

    cleanedFreq = freq[np.where(spectrum < Top)]
    cleanedSpectrum = spectrum[np.where(spectrum < Top)]

    idx = sig.find_peaks_cwt(cleanedSpectrum, widths)

    peaksPos = cleanedFreq[idx]
    peaksHeight = cleanedSpectrum[idx]

    return peaksPos, peaksHeight


def FitPeaks(freq, spectrum, shape, peakPos=0, width, guess, Top=101):
    # NOT IMPLEMENTED
    # Tries to fit the peaks found, can work on given peaks or automatically
    # search for peaks

    if shape is 'gaussian':
        return 0
    elif shape is 'lorentzian':
        return 0
    else:
        return 0

    if peakPos is 0:
        # call FindPeaks
        return 0
    elif peakPos > 0:
        # Find a way to extract only peaks from data
        return 0
