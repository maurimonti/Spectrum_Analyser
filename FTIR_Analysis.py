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
Comp = True  # If True takes a second set of data as comparison

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
date = '22Feb'
# The path can be directly modified in case
path = dataLocation + sample + "/" + month + year + "/" + date + "/"

# Names of the files to analyse

# Sample we are actually interested in:
nameSignal = 'LSMO_refl_NIR_CaF2_InGaAs_256scan_1cm-1_1mm_1.dpt'
# Comparison file (substrate for ex):
nameComp = 'LAO refl_NIR_CaF2_InGaAs_256scan_1cm-1_1mm_1.dpt'
# Reference:
nameRef = 'Au_refl_NIR_CaF2_InGaAs_256scan_1cm-1_1mm_1.dpt'
# Background measurement:
nameBack = 'Holder refl_NIR_CaF2_InGaAs_256scan_1cm-1_1mm_1.dpt'
# Background of the reference:
nameBackRef = 'Hole refl_NIR_CaF2_InGaAs_256scan_1cm-1_1mm_1.dpt'


Type = 'tab'  # Separator of the data: csv or tab or space


# Properties of the measurement
measurement = 'refl'  # Which type of measurement are we performing
xUnit = 'cm1'  # Flag for the unit to use for the x axis
yUnit = ''
plotType = 'logx'

# Definition of the parameters of the figure
legendSignal = 'LSMO'  # Legend entries
legendComp = ''

axisBounds = [5000, 20000, -5, 80]   # Axes limits

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


def main():
    # main of the script: calls the functions
    dataSignal = ftir.ReadFTIR(path + nameSignal, Type)
    dataRef = ftir.ReadFTIR(path + nameRef, Type)
    dataBack = ftir.ReadFTIR(path + nameBack, Type)
    dataBackRef = ftir.ReadFTIR(path + nameBackRef, Type)

    spectrum = ftir.Computer(dataSignal, dataRef, dataBack, dataBackRef,
                             Background)

    spectrumConverted = ftir.Converter(spectrum[0], spectrum[1], xUnit, yUnit)
    ftir.Normalizer(spectrumConverted[1], 0, False, 50)

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
