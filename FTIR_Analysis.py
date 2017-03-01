# This script is meant to be a simple software that reads plots and analyse
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
Comp = False  # If True takes a second set of data as comparison

# Definition of the path
Location = '/home/'
# These define the position of the files
dataLocation = Location + 'Data/'
# This is the subpath of the raw data
resLocation = Location + 'Results/'  # This is the subpath of the results
fileSep = '/'   # This is the path divider

sample = ''  # Names that define the position of the data:
# they are divided to allow easy modifications
month = 'February'
year = '2017'
date = '24Feb'
# The path can be directly modified in case
path = dataLocation + sample + "/" + month + year + "/" + date + "/"

# Names of the files to analyse

# Sample we are actually interested in:
nameSignal = 'signal.csv'
# Comparison file (substrate for ex):
nameComp = 'sub.csv'
# Reference:
nameRef = 'ref.csv'
# Background measurement:
nameBack = 'back.csv'
# Background of the reference:
nameBackRef = 'backref.csv'


Type = 'tab'  # Separator of the data: csv or tab or space


# Properties of the measurement
measurement = 'refl'  # Which type of measurement are we performing

# Definition of the parameters of the figure
legendSignal = ''  # Legend entries
legendComp = ''

axisBounds = [0.45, 1.11, 0, 40]   # Axes limits

shapeSignal = 'b'  # Colour and shape of the figure symbol
shapeComp = 'r'

# xlabel = '$k(cm^{-1})$'
# Labels of the figure, at the moment only micrometers are allowed
xlabel = '$\lambda(\mu m)$'
ylabel = '$r(\%)$'

title = ' reflectivity'  # Title of the figure

save = True  # If true saves the figure

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

    dataSignal = ftir.Converter(dataSignal[0], dataSignal[1])
    dataRef = ftir.Converter(dataRef[0], dataRef[1])
    dataBack = ftir.Converter(dataBack[0], dataBack[1])
    dataBackRef = ftir.Converter(dataBackRef[0], dataBackRef[1])

    spectrum = ftir.Computer(dataSignal, dataRef, dataBack, dataBackRef,
                             Background)

    plt.figure(1)
    plt.axis(axisBounds)
    plt.title(title, fontsize=24)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)

    ftir.plotter(spectrum[0], spectrum[1], shapeSignal, legendSignal)

    if Comp is True:
        dataComp = ftir.ReadFTIR(path + nameComp, Type)
        dataComp = ftir.Converter(dataComp[0], dataComp[1])
        spectrum = ftir.Computer(dataComp, dataRef, dataBack, dataBackRef,
                                 Background)
        ftir.plotter(spectrum[0], spectrum[1], shapeComp, legendComp)

    if save is True:
        plt.savefig(figPath + figName, dpi=None, facecolor='w', edgecolor='w',
                    orientation='landscape', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None)

    plt.legend()
    plt.show()

    # plt.figure(2)
    # plt.plot(dataRef[0],dataRef[1], dataSignal[0], dataSignal[1])
    # plt.show()
    return 1


if __name__ == '__main__':
    # Ridefinire tutte le funzioni del main in modo da parametrizzare tutto
    # cosi' che le funzioni diventino usabili per davvero, togliedno
    # riferimenti all'inizio dello script e lasciarli solo nel main
    # gia' che ci sono mi sposto tutte le funzioni in un altro file in modo
    # da fare anche meno casino
    main()
