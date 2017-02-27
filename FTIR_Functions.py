import csv
import sys
import numpy as np
import matplotlib.pyplot as plt


def Converter(xIn, yIn):
    # This function converts the x in \mu m (much better)
    # a modification of the intensity is also possible
    xOut = [x**(-1) * 10000 for x in xIn]
    yOut = yIn
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
        print 'damn! file type not recognized!'
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

    ratio = spectrum / spectrumRef * 100
    return data[0], ratio


def plotter(wavelength, spectrum, shape, name):
    # This function plots the data
    plt.plot(wavelength, spectrum, shape, label=name)

    return plt.figure(1)
