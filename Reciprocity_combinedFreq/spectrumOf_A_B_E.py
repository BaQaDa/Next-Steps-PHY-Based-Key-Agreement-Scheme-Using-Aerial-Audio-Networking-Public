import os
from matplotlib import ticker
from pylab import *
from scipy.fftpack import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.io import wavfile
from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter
from scipy.signal import find_peaks
import math


# function that returns correlation coefficient.
def correlationCoefficient(X, Y, n):
    sum_X = 0
    sum_Y = 0
    sum_XY = 0
    squareSum_X = 0
    squareSum_Y = 0

    i = 0
    while i < n:
        # sum of elements of array X.
        sum_X = sum_X + X[i]

        # sum of elements of array Y.
        sum_Y = sum_Y + Y[i]

        # sum of X[i] * Y[i].
        sum_XY = sum_XY + X[i] * Y[i]

        # sum of square of array elements.
        squareSum_X = squareSum_X + X[i] * X[i]
        squareSum_Y = squareSum_Y + Y[i] * Y[i]

        i = i + 1

    # use formula for calculating correlation
    # coefficient.
    corr = (float)(n * sum_XY - sum_X * sum_Y) /(float)(math.sqrt((n * squareSum_X -
                       sum_X * sum_X) * (n * squareSum_Y -
                                         sum_Y * sum_Y)))
    return corr


def normalize(array, x, y):
    m = array.min()
    range = array.max() - m
    array_temp = (array - m) / range
    range2 = y - x
    array_norm = (array_temp * range2) + x
    return array_norm

def spectrum_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order,
                          do_filter):
    output_path = input_path

    for num in range(1, numOfRounds + 1):
        num = 4
        image_name = str(num) + '-'+ str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spectrum'
        image_spectrum = os.path.join(output_path, image_name + '.png')

        fig2, (ax, ax1, ax2) = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
        fig3, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(9, 3), sharey=True)

        '''____________________ Alice ____________________'''

        file_name_Alice = str(num) + 'Alice' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Alice = os.path.join(input_path, file_name_Alice + '.wav')

        sampFreq_Alice, samples_Alice = wavfile.read(input_file_Alice)

        samples_Alice = butter_bandpass_filter(samples_Alice, lowcut, highcut, sampFreq_Alice, order=filter_order)
        num_samples = samples_Alice.shape[0]
        datafft = fft(samples_Alice)
        # Get the absolute value of real and complex component:
        fftabs = abs(datafft)
        fftabs_norm = normalize(fftabs, 0, 60)
        freqs = fftfreq(num_samples, 1 / sampFreq_Alice)
        scale_x = 1e3
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:1n}'.format(x / scale_x))
        ax.xaxis.set_major_formatter(ticks_x)
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        ax.tick_params(direction='in')
        ax.set_ylabel('Magnitude (energy)')
        # ax.set_xlabel('Frequency [KHz]')
        ax.set_title('B -> A')
        ax.plot(freqs[int(len(freqs)/8):int(freqs.size / 3.5)], fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)], linewidth=0.8, color='black')

        # Extract spectrum peaks at the tone frequencies
        x_Alice = fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)]
        peaks, _ = find_peaks(x_Alice, height=0.8, distance=240)
        ax3.plot(x_Alice)
        ax3.plot(peaks, x_Alice[peaks], "x")
        peaks_Alice = x_Alice[peaks]
        # print(num, '_', peaks_Alice)

        '''____________________ Bob ____________________'''

        file_name_Bob = str(num) + 'Bob' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Bob = os.path.join(input_path, file_name_Bob + '.wav')

        sampFreq_Bob, samples_Bob = wavfile.read(input_file_Bob)

        samples_Bob = butter_bandpass_filter(samples_Bob, lowcut, highcut, sampFreq_Alice, order=filter_order)
        num_samples = samples_Bob.shape[0]
        datafft = fft(samples_Bob)
        # Get the absolute value of real and complex component:
        fftabs = abs(datafft)
        fftabs_norm = normalize(fftabs, 0, 60)
        freqs = fftfreq(num_samples, 1 / sampFreq_Bob)

        scale_x = 1e3
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:1n}'.format(x / scale_x))
        ax1.xaxis.set_major_formatter(ticks_x)
        ax1.yaxis.set_ticks_position('both')
        ax1.xaxis.set_ticks_position('both')
        ax1.tick_params(direction='in')
        ax1.set_xlabel('Frequency [kHz]')
        ax1.set_title('A -> B')
        ax1.plot(freqs[int(len(freqs)/8):int(freqs.size / 3.5)], fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)], linewidth=0.8, color='black')


        # Extract spectrum peaks at the tone frequencies
        x_Bob = fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)]
        peaks, _ = find_peaks(x_Bob, height=0.8, distance=240)
        ax4.plot(x_Bob)
        ax4.plot(peaks, x_Bob[peaks], "x")
        peaks_Bob = x_Bob[peaks]
        # print(num, '_', peaks_Bob)

        '''____________________ Eve ____________________'''

        file_name_Eve = str(num) + 'Eve' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Eve = os.path.join(input_path, file_name_Eve + '.wav')

        sampFreq_Eve, samples_Eve = wavfile.read(input_file_Eve)

        samples_Eve = butter_bandpass_filter(samples_Eve, lowcut, highcut, sampFreq_Eve, order=filter_order)
        num_samples = samples_Eve.shape[0]
        datafft = fft(samples_Eve)
        # Get the absolute value of real and complex component:
        fftabs = abs(datafft)
        fftabs_norm = normalize(fftabs, 0, 60)
        freqs = fftfreq(num_samples, 1 / sampFreq_Eve)
        # print(len(freqs))
        scale_x = 1e3
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:1n}'.format(x / scale_x))
        ax2.xaxis.set_major_formatter(ticks_x)
        ax2.yaxis.set_ticks_position('both')
        ax2.xaxis.set_ticks_position('both')
        ax2.tick_params(direction='in')
        # ax2.set_xlabel('Frequency [KHz]')
        ax2.set_title('A -> E')
        ax2.plot(freqs[int(len(freqs)/8):int(freqs.size / 3.5)], fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)], linewidth=0.8, color='black')
        # ax2.text(0.05, 0.5, 'SPL [pascal]', va='center', rotation='vertical',  size=9)


        # Extract spectrum peaks at the tone frequencies
        x_Eve = fftabs_norm[int(len(freqs)/8):int(freqs.size / 3.5)]
        peaks, _ = find_peaks(x_Eve, height=0.3, distance=240)
        ax5.plot(x_Eve)
        ax5.plot(peaks, x_Eve[peaks], "x")
        peaks_Eve = x_Eve[peaks]
        # print(num, '_', peaks_Eve)

        fig2.savefig(image_spectrum,  bbox_inches='tight')
        plt.show()

        # Find the size of array.
        n = len(peaks_Alice)
        # Function call to correlationCoefficient. (AB_BA)
        AB_BA_CorrCoef = '{0:.6f}'.format(correlationCoefficient(peaks_Bob, peaks_Alice, n))
        print(num, ' AB_BA_CorrCoef: ', AB_BA_CorrCoef)

        # Function call to correlationCoefficient. (AE_BA)
        AE_BA_CorrCoef = '{0:.6f}'.format(correlationCoefficient(peaks_Eve, peaks_Alice, n))
        print(num, 'AB_AE_CorrCoef: ', AE_BA_CorrCoef)


if (__name__) == "__main__":
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\room-multi-freq"
    input_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\Exps_paper\\room-multi-freq"


    start_freq, freq_num, freq_gap = 8000, 15, 250
    lowcut, highcut = start_freq - 10, start_freq + ((freq_num - 1) * freq_gap) + 10
    filter_order = 4
    numOfRounds = 4
    do_filter = 'True'

    spectrum_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order, do_filter)

