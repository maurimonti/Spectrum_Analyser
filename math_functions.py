import numpy as np  # No need to explain this
import sympy as sym  # symbolic calculations
import sys  # System library used for exit



def FFT(xData, yData, xUnit=0):
    # Computes the FFT of the data and returns the frequency and the spectrum
    # xUnit used to convert the xData in frequency depending on the unit of
    # the x (mm or seconds, not implemented yet)

    yfft = np.fft.fft(yData)
    fftLen = len(yfft)
    yfft = yfft[0:(fftLen / 2 + 1)]
    cvf = 0.1499

    timeStep = abs(xData[fftLen - 1] - xData[0]) / (fftLen - 1) / cvf
    freq = np.array(range(fftLen / 2 + 1)) / timeStep / fftLen

    return freq, yfft


def IFFT(xData, yData, xUnit=0):
    # Computes the inverse FFT of the data and returns the frequency and the
    # spectrum
    # xUnit used to convert the xData in frequency depending on the unit of
    # the x (mm or seconds, not implemented yet)

    yifft = np.fft.ifft(yData)
    fftLen = len(yifft)
    yifft = yifft[0:(fftLen / 2 + 1)]
    cvf = 0.1499

    timeStep = abs(xData[fftLen - 1] - xData[0]) / (fftLen - 1) / cvf
    freq = np.array(range(fftLen / 2 + 1)) / timeStep / fftLen

    return freq, yifft


def SymHessian(f, x, y):
    # Computes and returns the symbolic Hessian
    # of a scalar function of two variables
    # f: functions to differentiate
    # x, y variables to respect with differentiate

    H = [[[], []], [[], []]]
    H[0][0] = sym.diff(f, x, x)
    H[0][1] = sym.diff(f, x, y)
    H[1][0] = sym.diff(f, y, x)
    H[1][1] = sym.diff(f, y, y)

    return H


def SymGradient(f, x, y):
    # Computes and returns the symbolic gradient
    # of a scalar function of two variables
    # f: functions to differentiate
    # x, y variables to respect with differentiate

    D = [[], []]
    D[0] = sym.diff(f, x)
    D[1] = sym.diff(f, y)

    return D


def Gradient(f, step):
    # Computes the gradient of the provided function x
    # step is the x step (assumed equal for all variables)

    xGrad = np.gradient(f)
    gradient = xGrad / step

    return gradient


def Hessian(x, step1, step2):
    # Returns the numerical 2 variable Hessian of the function
    # step 1 and step 2 are the spacing of the two variables

    xGrad = np.gradient(x)
    hessian = np.empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype)
    for k, kgrad in enumerate(xGrad):
        tmp_grad = np.gradient(kgrad)
        for l, grad_kl in enumerate(tmp_grad):
            hessian[k, l, :, :] = grad_kl / (step1 * step2)
    return hessian


def WavenumberConverter(wn, out='nm'):
        # Stupid functions that converts wavenumbers in a chosen unit
        # default nanometers

        if out is 'micro':
                xOut = [x**(-1) * 10000 for x in wn]

        elif out is 'nm':
                xOut = [x**(-1) * 10000000 for x in wn]

        elif out is 'eV':
                xOut = [x * 1.23984 * 0.0001 for x in wn]
        else:
                sys.exit('Damn! Unit not recognized!')

        return xOut
