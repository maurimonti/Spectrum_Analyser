# This script is meant to be a simple software that reads plots and analyse
# the data from the FTIR

# The name Signal refers to the sample we are interested in,
# the name Comp refers to the sample used as comparison
# (for example a substrate)
# the name Ref refers to the reference (for ex. a gold mirror)

# Modules
import csv
import matplotlib.pyplot as plt
import sys
from matplotlib import rc
import numpy as np


# ## Global variables definitions###

Background = True  # If True subtracts a background from the data

# Definition of the path
Location = '/home/mmonti/Documents/Phd/'
# These define the position of the files
dataLocation = Location + 'Data/'
# This is the subpath of the raw data
resLocation = Location + 'Results/'  # This is the subpath of the results
fileSep = '/'   # This is the path divider

sample = 'LSMO'  # Names that define the position of the data:
# they are divided to allow easy modifications
month = 'February'
year = '2017'
date = '16Feb'
# The path can be directly modified in case
path = dataLocation + sample + "/" + month + year + "/" + date + "/"

# Names of the files to analyse

# Sample we are actually interested in:
nameSignal = 'LSMO-LAO_refl_NIR_visQ_SiDiode_256scan_1cm-1.dpt'
# Comparison file (substrate for ex):
nameComp = 'LAO_refl_NIR_visQ_SiDiode_256scan_1cm-1.dpt'
# Reference:
nameRef = 'ref_Au_refl_NIR_visQ_SiDiode_256scan_1cm-1.dpt'  
# Background measurement:
nameBack = 'ref_Holder_refl_NIR_visQ_SiDiode_256scan_1cm-1.dpt'
# Background of the reference:
nameBackRef = 'ref_Hole_refl_NIR_visQ_SiDiode_256scan_1cm-1.dpt'


Type = 'tab'  # Separator of the data: csv or tab or space


# Properties of the measurement
measurement = 'refl'  # Which type of measurement are we performing

# Definition of the parameters of the figure
legendSignal = 'LSMO'  # Legend entries
legendComp = 'LAO'

axisBoundsSignal = [0.45, 1.1, 0, 35]   # Axes limits
axisBoundsComp = [0.45, 1.1, 0, 35]

shapeSignal = 'b'  # Colour and shape of the figure symbol
shapeComp = 'r'

# xlabel = '$k(cm^{-1})$'
# Labels of the figure, at the moment only micrometers are allowed
xlabel = '$\lambda(\mu m)$'
ylabel = '$r(\%)$'

title = 'LSMO reflectivity'  # Title of the figure

save = False  # If true saves the figure

figPath = (resLocation + fileSep +
           sample + fileSep +
           month + year + fileSep +
           date + fileSep)  # Position of the figure

figName = ('FTIR_' + measurement + '_' +
           legendSignal + '_' + legendComp + '.pdf')  # Name of the figure


#########################################
# ## DO NOT TOUCH ANYTHING FROM HERE ## #
#########################################


rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# defines the font of matplotlib: nedded for using latex
rc('text', usetex=True)  # Allows the use of latex


def Converter(xIn, yIn):
    # This function converts the x in \mu m (much better)
    # a modification of the intensity is also possible
    xOut = [x**(-1) * 10000 for x in xIn]
    yOut = yIn
    out = np.array([xOut, yOut])

    return out


def Opener(path):
    # this function open the file and put them into a list
    dati = []
    if Type is 'csv':
        with open(path) as f:
            dati = list(csv.reader(f))

    elif Type is 'tab' or 'space':
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                columns = line.split()
                dati.append(columns)

    return dati


def ReadFTIR(path):
    # This function reads the file of the FTIR and return them in an array

    numeri = []
    inten = []

    try:
        dati = Opener(path)
        for x in dati:
            for y in x:
                if x.index(y) == 0:
                    numeri.append(float(y))
                if x.index(y) == 1:
                    inten.append(float(y))

    except:
        print 'file type not recognized!'
        sys.exit()

    data = np.array([numeri, inten])

    return data


def plotter(data, dataRef, name, axisBounds,
            title, shape, dataBack, dataBackRef):
    # This function plots the data
    wavenumber = data[0]
    ratio = []
    if Background is True:
        spectrum = data[1] - dataBack[1]
        spectrumRef = dataRef[1] - dataBackRef[1]

    elif Background is False:
        spectrum = data[1]
        spectrumRef = dataRef[1]

    ratio = spectrum / spectrumRef * 100
    plt.figure(1)
    plt.plot(wavenumber, ratio, shape, label=name)
    plt.axis(axisBounds)
    plt.title(title, fontsize=24)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.legend()

    return plt.figure(1)


def figureManager(figure):
    # This function shows the plot and, if save is true, saves it
    if save is True:
        plt.savefig(figPath + figName, dpi=None, facecolor='w', edgecolor='w',
                    orientation='landscape', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None)

    plt.show()


def main():
    # main of the script: calls the functions
    dataSignal = ReadFTIR(path + nameSignal)
    dataComp = ReadFTIR(path + nameComp)
    dataRef = ReadFTIR(path + nameRef)
    dataBack = ReadFTIR(path + nameBack)
    dataBackRef = ReadFTIR(path + nameBackRef)

    dataSignal = Converter(dataSignal[0], dataSignal[1])
    dataComp = Converter(dataComp[0], dataComp[1])
    dataRef = Converter(dataRef[0], dataRef[1])
    dataBack = Converter(dataBack[0], dataBack[1])
    dataBackRef = Converter(dataBackRef[0], dataBackRef[1])

    figureSignal = plotter(dataSignal, dataRef, legendSignal,
                           axisBoundsSignal, title, shapeSignal,
                           dataBack, dataBackRef)
    figure = plotter(dataComp, dataRef, legendComp,
                     axisBoundsComp, title, shapeComp, dataBack, dataBackRef)

    figureManager(figure)
    return 1


if __name__ == '__main__':
    main()
