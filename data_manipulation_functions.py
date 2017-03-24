import sys  # system methods, used for exit
import numpy as np  # Do I really have to explain that?
import matplotlib.pyplot as plt  # plotting
import scipy.signal as sig  # library with signal analysis (find peaks, et.)

import lmfit as fit  # Fit library

import math_functions as mt  # Library for mathematical stuff


# All the functions used for manipulating the data


def Reader(path, comment='%', delimiter='\t', skipRows=0):
    # Self-explaining: reads a text file and puts the data into an array
    try:
        data = np.loadtxt(path,
                          comments=comment,
                          delimiter=delimiter,
                          skiprows=skipRows,
                          unpack=True)
    except IOError:
        sys.exit('Damn! File not found!')

    return data


def Shifter(xData, xDataRef):
    # Shifts one data series to align it with a second one, returns the
    # aligned data

    delta = xData[0] - xDataRef[0]  # no abs, it's sign-wise
    xOut = xData - delta
    xOutRef = xDataRef

    return xOut, xOutRef


def Computer(data, dataRef, dataBack=[], dataBackRef=[], Back=False):
    # This function computes the reflectivity spectrum dividing the raw data
    # for a given reference. If Back is True also subtract a given background
    # to compensate for a non good alignment or for a non good aperture size.
    # Returns the spectrum

    ratio = np.zeros(len(data))
    if Back is True:
        spectrum = data - dataBack
        spectrumRef = dataRef - dataBackRef

    elif Back is False:
        spectrum = data
        spectrumRef = dataRef

    ratio = spectrum / spectrumRef
    return ratio


def plotter(wavelength, spectrum, shape, name, flag='normal'):
    # This function plots the data, depending on the value of flag changes
    # the plot type.
    # Returns the plot

    if flag is 'normal':
        outPlot = plt.plot(wavelength, spectrum, shape, label=name)
    elif flag is 'logx':
        outPlot = plt.semilogx(wavelength, spectrum, shape, label=name)
    elif flag is 'logy':
        outPlot = plt.semilogy(wavelength, spectrum, shape, label=name)
    elif flag is 'loglog':
        outPlot = plt.loglog(wavelength, spectrum, shape, label=name)
    else:
        sys.exit('damn! plot type non recognized!')

    return outPlot


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
            maximaVal = maximaVal[np.where(maximaVal < theoMax)]  # deletes
            maxVal = np.nanmax(maximaVal)                         # spikes
            out = spectrum / maxVal
            return out

        else:
            sys.exit('WTF? I don\'t know how the noise is!')

    elif default < 0:
        sys.exit('Damn! Normalization value is negative!')

    else:
        out = spectrum / default
        return out


def Converter(xIn, yIn, xFormat, yFormat, xUnit, yUnit):
    # This function converts the x and y in a chosen unit that depends on the 
    # xUnit and yUnit values. xFormat is the input format, yFormat is not
    # implemented yet
    # Returns the converted data

    if xFormat is 'cm1':

        if xUnit is not 'cm1':
            xOut = mt.WavenumberConverter(xIn, xUnit)
        elif xUnit is 'cm1':
            xOut = [x for x in xIn]

    if xFormat is 'mm':

        if xUnit is 'THz':
            xOut = xIn
        else:
            sys.exit('damn! Unit of measure of x not recognized!')
    if yUnit is '':
        yOut = yIn

    if yUnit is '%':
        yOut = [y * 100 for y in yIn]

    out = np.array([xOut, yOut])

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


def LabelAssigner(xUnit, yUnit='%', meas='reflection'):
    # Self-explaining receives the unit chosen and returns the correct label

    if xUnit is 'cm1':
        xlabel = '$k(cm^{-1})$'
    elif xUnit is 'nm':
        xlabel = '$\lambda(nm)$'
    elif xUnit is 'micro':
        xlabel = '$\lambda(\mu m)$'
    elif xUnit is 'eV':
        xlabel = '$E(eV)$'
    elif xUnit is 'THz':
        xlabel = '$\\nu(THz)$'
    if meas is 'reflection':
        if yUnit is '%':
            ylabel = '$r(\%)$'
        elif yUnit is '':
            ylabel = '$r$'
    elif meas is 'transmission':
        if yUnit is '%':
            ylabel = '$t(\%)$'
        elif yUnit is '':
            ylabel = '$t$'

    return xlabel, ylabel


def FitPeaks(freq, spectrum, shape, peakPos, width, guess=1, N=3, Top=101):
        # NOT IMPLEMENTED
        # Tries to fit the peaks found, can work on given peaks or
        # automatically search for peaks (maybe)

        if shape is 'gaussian':
                mod = fit.models.GaussianModel()
        elif shape is 'lorentzian':
                mod = fit.model.lorentzian()
        else:
                sys.exit('Damn! Model not found!')

        # extract peaks
        step = freq[1] - freq[0]
        numPeaks = len(peakPos)
        dataPeaks = np.zeros(numPeaks, 2,
                             np.ceil(2 * N * np.amax(width) / step))
        for i in xrange(0, numPeaks):
                dataPeaks[i][0] = freq[
                    np.where(
                        np.abs(freq - peakPos[i]) < N * width[i])]
                dataPeaks[i][1] = spectrum[
                    np.where(
                        np.abs(freq - peakPos[i]) < N * width[i])]
        # fit peaks
        pars = np.zeros(numPeaks)
        out = np.zeros(numPeaks)
        for i in xrange(0, numPeaks):
                pars[i] = mod.guess(dataPeaks[i][1], x=dataPeaks[i][0])
                out[i] = mod.fit(dataPeaks[i][1], pars[i], x=dataPeaks[i][0])
        return out
