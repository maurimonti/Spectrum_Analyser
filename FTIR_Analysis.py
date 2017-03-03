 This script is meant to be a simple software that reads plots and analyse
# the data from the FTIR

# The name Signal refers to the sample we are interested in,
# the name Comp refers to the sample used as comparison
# (for example a substrate)
# the name Ref refers to the reference (for ex. a gold mirror)

# Modules
import matplotlib.pyplot as plt
from matplotlib import rc
import FTIR_Functions as ftir


# ## Global variables definitions## #

Background = True  # If True subtracts a background from the data
Comp = True  # If True takes a second set of data as comparison

# Definition of the path
Location = ''
# These define the position of the files
dataLocation = Location + 'Data/'
# This is the subpath of the raw data
resLocation = Location + 'Results/'  # This is the subpath of the results
fileSep = '/'   # This is the path divider

sample = ''  # Names that define the position of the data:
# they are divided to allow easy modifications
month = 'February'
year = '2017'
date = '22Feb'
# The path can be directly modified in case
path = dataLocation + sample + "/" + month + year + "/" + date + "/"

# Names of the files to analyse

# Sample we are actually interested in:
nameSignal = 'Signal.dpt'
# Comparison file (substrate for ex):
nameComp = 'Comp.dpt'
# Reference:
nameRef = 'Ref.dpt'
# Background measurement:
nameBack = 'Back.dpt'
# Background of the reference:
nameBackRef = 'BackRef.dpt'


Type = 'tab'  # Separator of the data: csv or tab or space


# Properties of the measurement
measurement = 'refl'
xUnit = 'cm1'  # Flag for the unit to use for the x axis:
# cm1 for cm**-1,
# nm for nanometers
# micro for micrometers ($\mu m$)
# eV for electronvolts
yUnit = ''  # flag for the y axis unit not implemented yet!
plotType = 'logx'  # flag for the plot type:
# normal for a normal linear plot,
# logx for a semilogx plot
# logy for a semilogy plot
# loglog for a log log plot

# Definition of the parameters of the figure
legendSignal = ''  # Legend entries
legendComp = ''

axisBounds = [5000, 20000, -5, 80]   # Axes limits

shapeSignal = 'b'  # Colour and shape of the figure symbol
shapeComp = 'r'

# Labels of the figure will be soon replace by an automatic label dependent
# on the unit chosen
xlabel = '$k(cm^{-1})$'
ylabel = '$r(\%)$'

title = 'reflectivity'  # Title of the figure

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


def main():
    # main of the script: calls the functions
    dataSignal = ftir.ReadFTIR(path + nameSignal, Type)
    dataRef = ftir.ReadFTIR(path + nameRef, Type)
    dataBack = ftir.ReadFTIR(path + nameBack, Type)
    dataBackRef = ftir.ReadFTIR(path + nameBackRef, Type)

    spectrum = ftir.Computer(dataSignal, dataRef, dataBack, dataBackRef,
                             Background)

    spectrumConverted = ftir.Converter(spectrum[0], spectrum[1], xUnit, yUnit)

    plt.figure(1)

    ftir.plotter(spectrumConverted[0], spectrumConverted[1],
                 shapeSignal, legendSignal, plotType)

    if Comp is True:
        dataComp = ftir.ReadFTIR(path + nameComp, Type)

        spectrum = ftir.Computer(dataComp, dataRef, dataBack, dataBackRef,
                                 Background)

        spectrumConverted = ftir.Converter(spectrum[0], spectrum[1],
                                           xUnit, yUnit)

        ftir.plotter(spectrumConverted[0], spectrumConverted[1],
                     shapeComp, legendComp, plotType)

    if save is True:
        plt.savefig(figPath + figName, dpi=None, facecolor='w', edgecolor='w',
                    orientation='landscape', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None)

    plt.axis(axisBounds)
    plt.title(title, fontsize=24)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.legend()
    plt.show()

    return 1


if __name__ == '__main__':
    # plotting also the raw signals
    main()
