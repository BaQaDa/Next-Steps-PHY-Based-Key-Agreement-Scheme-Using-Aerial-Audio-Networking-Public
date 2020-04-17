import os

from matplotlib import ticker
from pylab import *
from scipy.fftpack import fft,fftfreq
import matplotlib.pyplot as plt
from scipy.io import wavfile


if __name__ == '__main__':

    file_name = '2Eve0-1-0'

    '''Original Received Signal
       ------------------------'''
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Used_AmbientNoise-My Spectrum function"
    input_file = os.path.join(input_path, file_name + '.wav')
    output_path = input_path

    sampFreq, s1 = wavfile.read(input_file)
    start_freq, freq_num, freq_gap = 0, 1, 0


    n = len(s1)
    p = fft(s1)  # take the fourier transform

    nUniquePts = int(ceil((n + 1) / 2.0))
    p = p[0:nUniquePts]
    p = abs(p)

    p = p / float(n)  # scale by the number of points so that
    # the magnitude does not depend on the length
    # of the signal or on its sampling frequency
    p = p ** 2  # square it to get the power

    # multiply by two (see technical document for details)
    # odd nfft excludes Nyquist point
    if n % 2 > 0:  # we've got odd number of points fft
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) - 1] = p[1:len(p) - 1] * 2  # we've got even number of points fft

    freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n)
    plot(freqArray / 1000, 10 * log10(p), color='k')
    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')




    plt.show()

