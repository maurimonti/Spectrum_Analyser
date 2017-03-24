import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


import data_manipulation_functions as man
import math_functions as mt

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# defines the font of matplotlib: nedded for using latex
rc('text', usetex=True)  # Allows the use of latex

# ## Global variables definitions## #

background = True  # If True subtracts a background from the data
comp = True  # If True takes a second set of data as comparison
fft = False  # if true assumes the data be time-domain and does an fft

# Definition of the path
fileSep = '/'
location = '/home/'
dataLocation = location + 'Data/'
resLocation = location + 'Results/'

sample = ''
month = ''
date = ''

dataPath = dataLocation + sample + fileSep + month + fileSep + date + fileSep
resPath = resLocation + sample + fileSep + month + fileSep + date + fileSep


nameSignal = ''  # Sample we are actually interested in:
nameComp = ''  # Comparison file (substrate for ex):
nameRef = ''  # Reference
nameBack = ''  # Background measurement:
nameBackRef = ''  # Background of the reference:

delimiter = '\t'  # Delimiter of the file

# Measurement properties
xFormat = 'cm1'  # Format of the x input
measurement = 'reflection'  # Which measurement are we performin: trans or refl

# Plot properties
xUnit = 'nm'  # Flag for the unit to use for the x axis:
# cm1 for cm**-1,
# nm for nanometers
# micro for micrometers ($\mu m$)
# eV for electronvolts

yUnit = '%'  # flag for the y axis:
# '' for simple reflection/transmission values
# '%' for percentage

plotType = 'normal'  # flag for the plot type:
# normal for a normal linear plot,
# logx for a semilogx plot
# logy for a semilogy plot
# loglog for a log log plot

xmin = 1000  # Limits of the axes
xmax = 2500
ymin = 0
ymax = 100


# Data saving properties
save = False  # if True saves the data
figName = (measurement + '_' + sample + '.pdf')  # name of figure and file
fileName = (measurement + '_' + sample + '.txt')


###############################################################################

###############################################################################

def Spectrum_Analyser(path=dataPath,
                      nameSignal=nameSignal,
                      nameRef=nameRef,
                      nameBack=nameBack,
                      nameBackRef=nameBackRef,
                      delimiter=delimiter,
                      background=background,
                      comp=comp,
                      xUnit=xUnit,
                      yUnit=yUnit,
                      plotType=plotType,
                      save=save,
                      fft=fft):
# Main function of the script: now callable from other programs

    if fft is True:
        datax, datay = man.Reader(dataPath + nameSignal)
        dataRefx, dataRefy = man.Reader(dataPath + nameRef)

        datax, dataRefx = man.Shifter(datax, dataRefx)

        x, y = mt.FFT(datax, datay)
        xRef, yRef = mt.FFT(dataRefx, dataRefy)

        dataSignal = np.array([x, y])
        dataRef = np.array([xRef, yRef])
        background = False
        comp = False

        figNameDef = 'FFT_' + figName
        fileNameDef = 'FFT_' + fileName
    elif fft is False:
        dataSignal = man.Reader(dataPath + nameSignal)
        dataRef = man.Reader(dataPath + nameRef)
        figNameDef = figName
        fileNameDef = fileName

    if background is True:
        dataBack = man.Reader(path + nameBack, delimiter=delimiter)
        dataBackRef = man.Reader(path + nameBackRef, delimiter=delimiter)

    elif background is not True:
        dataBack = np.zeros([2, len(dataSignal[1])])
        dataBackRef = np.zeros([2, len(dataSignal[1])])

    spectrum = man.Computer(dataSignal[1],
                            dataRef[1],
                            dataBack[1],
                            dataBackRef[1],
                            background)

    if fft is True:
        spectrum = np.array([x, np.abs(y / yRef)])
        spectrumConverted = man.Converter(spectrum[0], spectrum[1],
                                          xFormat, '',
                                          xUnit, yUnit)
    elif fft is False:
        spectrumConverted = man.Converter(dataSignal[0], spectrum,
                                          xFormat, '',
                                          xUnit, yUnit)

    plt.figure(1)

    man.plotter(spectrumConverted[0], spectrumConverted[1],
                'b', sample, plotType)

    if comp is True:
        dataComp = man.Reader(path + nameComp, delimiter=delimiter)

        spectrum = man.Computer(dataComp[1],
                                dataRef[1],
                                dataBack[1],
                                dataBackRef[1],
                                background)

        spectrumConverted = man.Converter(dataComp[0], spectrum,
                                          xFormat, '',
                                          xUnit, yUnit)

        man.plotter(spectrumConverted[0], spectrumConverted[1],
                    'r', 'substrate', plotType)

    xlabel, ylabel = man.LabelAssigner(xUnit, yUnit, measurement)

    plt.axis([xmin, xmax, ymin, ymax])
    plt.title(sample + ' ' + measurement, fontsize=24)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)

    if save is True:
        plt.savefig(resPath + figNameDef, dpi=None, facecolor='w',
                    edgecolor='w', orientation='landscape', papertype=None,
                    format=None, transparent=False, bbox_inches=None,
                    pad_inches=0.1, frameon=None)
        if fft is True:
            np.savetxt(resPath + fileNameDef,
                       np.transpose([x, y, yRef, spectrum[1]]),
                       fmt='%8f', delimiter='\t',
                       header='f\t fft\t fftRef\t trans', comments='%')
    plt.show()

    return spectrumConverted


if __name__ == '__main__':
    # Calls the main
    Spectrum_Analyser()
