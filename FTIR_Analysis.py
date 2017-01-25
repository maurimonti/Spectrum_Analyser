# This script is meant to be a simple software that reads plots and analyse 
# the data from the FTIR

# The name Signal refers to the sample we are interested in, 
# the name Comp refers to the sample used as comparison (for example a substrate)
# the name Ref refers to the reference (for ex. a gold mirror)

# Modules
import csv
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np


### Global variables definitions###

# Definition of the path
Location = '/home/mmonti/Documents/Phd/'#These define the position of the files
dataLocation = Location + 'Data/'# This is the subpath of the raw data
resLocation = Location + 'Results/'# This is the subpath of the results
fileSep = '/' # This is the path divider

sample = 'LSMO'# Names that define the position of the data: they are divided to allow easy modifications
month = 'November'
year = '2016'
date = '25Nov'
# The path can be directly modified in case
path = dataLocation + sample + "/" + month + year + "/" + date + "/"

# Names of the files to analyse
nameSignal = 'LSMO-AC19-refl-MIR-KBr-DLaTGS-10scans-4cm-1-3mmAperture.dpt'# Sample we are actually interested in
nameComp = 'LAO-refl-MIR-KBr-DLaTGS-10scans-4cm-1-3mmAperture.dpt'# Comparison file (substrate for ex)
nameRef = 'Au-refl-MIR-KBr-DLaTGS-10scans-4cm-1-3mmAperture.dpt'# Reference


# Properties of the measurement
measurement = 'refl' # Which type of measurement are we performing

# Definition of the parameters of the figure
legendSignal = 'LSMO' # Legend entries
legendComp = 'LAO'

axisBoundsSignal = [10,33,0,60] # Axes limits
axisBoundsComp = [10,33,0,60]

shapeSignal = 'b' # Color and shape of the figure symbol
shapeComp = 'r'

# xlabel = '$k(cm^{-1})$' # Labels of the figure, at the moment only micrometers are allowed
xlabel = '$\lambda(\mu m)$'
ylabel = '$r(\%)$'

title = 'LSMO reflectivity' # Title of the figure

save = False # If true saves the figure

figPath = resLocation + fileSep + sample + fileSep + month + year + fileSep + date + fileSep # Position of the figure

figName =  'FTIR_' + measurement + '_' + legendSignal + '_' + legendComp + '.pdf' # Name of the figure


#######################################
### DO NOT TOUCH ANYTHING FROM HERE ###
#######################################



rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})# defines the font of matplotlib: nedded for using latex
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)# Allows the use of latex

#Prossima funzione deve prendere l'array 2d data e sputare fuori la x in una unita' di misura decente e forse la y in percentuale
def Converter(xIn,yIn):
# This function converts the x in \mu m (much better) a modification of the intensity is also possible
    xOut = [x**(-1)*10000 for x in xIn] 

    yOut = yIn
    out = np.array([xOut,yOut])
    return out

def ReadFTIR(path):
#This function reads the file of the FTIR and return them in an array
    numeri=[]
    inten=[]
    with open(path) as f:
        lettura = csv.reader(f)
        dati = list(lettura)

    for x in dati:
        for y in x:
            if x.index(y)==0:
                numeri.append(float(y))
            if x.index(y)==1:
                inten.append(float(y))

    data = np.array([numeri, inten])

    return data


def plotter (data,dataRef,name,axisBounds,title,shape):
# This function plots the data
    wavenumber = data[0]
    spectrum = data[1]
    wavenumberRef = dataRef[0]
    spectrumRef = dataRef[1]

    ratio = spectrum/spectrumRef*100
    #if r == 0:
    plt.figure(1)
    ratioPlot = plt.plot(wavenumber,ratio, shape, label=name)
    plt.axis(axisBounds)
    plt.title(title, fontsize=24)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tick_params(axis='both',which='major', labelsize=14)
    plt.legend()
    
    return plt.figure(1)


def figureManager(figure):
# This function shows the plot and, if save is ture, saves it
    if save == True:
        plt.savefig(figPath+figName, dpi=None, facecolor='w', edgecolor='w',
                orientation='landscape', papertype=None, format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None)
    
    plt.show()
    

if __name__ == '__main__':
# main of the script: calls the functions
    dataSignal = ReadFTIR(path+nameSignal)
    dataComp = ReadFTIR(path+nameComp)
    dataRef = ReadFTIR(path+nameRef)

    dataSignal = Converter(dataSignal[0],dataSignal[1])
    dataComp = Converter(dataComp[0],dataComp[1])
    dataRef = Converter(dataRef[0],dataRef[1])
    
    figureSignal = plotter(dataSignal,dataRef,legendSignal,
                           axisBoundsSignal,title,shapeSignal)
    figure = plotter(dataComp,dataRef,legendComp, 
                     axisBoundsComp,title,shapeComp)

    figureManager(figure)

