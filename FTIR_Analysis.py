# This script is meant to be a simple software that reads plots and analyse 
# the data from the FTIR

# The name Signal refers to the sample we are interested in, 
# the name Comp refers to the sample used as comparison (for example a substrate)
# the name Ref refers to the reference (for ex. a gold mirror)

# Modules
import csv
import matplotlib.pyplot as plt
import numpy as np


### Global variables definitions###

# dDefinition of the path
Location = ''#These define the position of the files
dataLocation = Location + 'Data/'# This is the subpath of the raw data
resLocation = Location + 'Results/'# This is the subpath of the results
fileSep = '/' # This is the path divider


# The path can be directly modified in case, it refers to the raw data position
path = dataLocation

# Names of the files to analyse
nameSignal = 'nameSignal.csv'# Sample we are actually intrested in
nameComp = 'nameComp.csv'# Comparison file (substrate for ex)
nameRef = 'nameRef.csv'# Reference


# Properties of the measurement
measurement = 'refl' # Which type of measurement are we performing

# Definition of the parameters of the figure
legendSignal = '' # Legend entries
legendComp = ''

axisBoundsSignal = [0,5000,0,1] # Axes limits
axisBoundsComp = [0,5000,0,1]

shapeSignal = 'b' # Color and shape of the figure symbol
shapeComp = 'r'

xlabel = 'k' # Labels of the figure, at the moment only wavenumbers are allowed
ylabel = 'r(%)'

title = '' # Title of the figure

save = False # If true saves the figure

figPath = resLocation  # Position of the figure

figName =  'FTIR_' + measurement + '_' + legendSignal + '_' + legendComp + '.pdf' # Name of the figure


##########################
### Functions and main ###
##########################

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

    ratio = spectrum/spectrumRef
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
    
    figureSignal = plotter(dataSignal,dataRef,legendSignal,
                       axisBoundsSignal,title,shapeSignal)
    figure = plotter(dataComp,dataRef,legendComp, 
                     axisBoundsComp,title,shapeComp)

    figureManager(figure)

 
