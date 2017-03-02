import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

def Converter(xIn, yIn, xUnit, yUnit):
    # This function converts the x in \mu m (much better)
    # a modification of the intensity is also possible
    if xUnit is 'micro':
        xOut = [x**(-1) * 10000 for x in xIn]

    elif xUnit is 'nm':
        xOut = [x**(-1) * 10000000 for x in xIn]

    elif xUnit is 'eV':
        xOut = [x * 1.23984 * 0.0001 for x in xIn]

    elif xUnit is 'cm1':
        xOut = [x for x in xIn]

    else:
        print 'damn! Unit of measure not recognized or not implemented!\n'
        sys.exscholarit()

    yOut = [y * 100 for y in yIn]
    out = np.array([xOut, yOut])

    return out


def Opener(pathFile, sep):
    # this function open the file and put them into a list
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


def ReadFTIR(pathFile, sep):
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
        print 'damn! file type not recognized!\n'
        sys.exscholarit()

    data = np.array([numeri, inten])

    return data


def Computer(data, dataRef, dataBack, dataBackRef, Back):
    ratio = []
    if Back is True:
        spectrum = data[1] - dataBack[1]
        spectrumRef = dataRef[1] - dataBackRef[1]

    elif Back is False:
        spectrum = data[1]
        spectrumRef = dataRef[1]

    ratio = spectrum / spectrumRef
    return data[0], ratio


def plotter(wavelength, spectrum, shape, name, flag):
    # This function plots the data
    if flag is 'normal':
        figure = plt.plot(wavelength, spectrum, shape, label=name)
    elif flag is 'logx':
        figure = plt.semilogx(wavelength, spectrum, shape, label=name)
    elif flag is 'logy':
        figure = plt.semilogy(wavelength, spectrum, shape, label=name)
    elif flag is 'loglog':
        figure = plt.loglog(wavelength, spectrum, shape, label=name)
    else:
        print 'damn! plot type non recognized!\n'

    return figure


def Normalizer(spectrum, default, noisy, theoMax):
    if default is 0:
        if noisy is False:
            maxVal = np.nanmax(spectrum)
            out = spectrum / maxVal
            return out
        elif noisy is True:
            maximaVal = spectrum[sig.argrelmax(spectrum)]
            maximaVal = maximaVal[np.where(maximaVal < theoMax)]
            out = np.nanmax(maximaVal)
            return out
        else:
            sys.exit('WTF? I don\'t know how the noise is!')
    elif default < 0:
        print 'Damn! Normalization value is negative!'
        sys.exit('Damn! Normalization value is negative!')

    else:
        out = spectrum / default
        return out
