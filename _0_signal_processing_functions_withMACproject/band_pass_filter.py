import os
from pylab import *
from scipy.io import wavfile
from scipy.signal import butter, lfilter

from _0_signal_processing_functions.plot_get_magnitude_spectrum import get_magnitude_spectrum

'''
For information about the function usage, check: 
1.  https://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html
2.  https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html
'''


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def plot_signal(samplerate, samples, plot_title):
    timeArray = arange(0, len(samples), 1)
    timeArray = timeArray / samplerate
    timeArray = timeArray * 1000  # scale to milliseconds
    plt.figure(figsize=(6, 4))
    plt.plot(timeArray, samples, 'y')
    plt.grid(True)
    plt.title(plot_title)
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



if __name__ == '__main__':

    # file_name = '1Alice15450-1-0'
    file_name = '1Bob15450-1-0'

    input_path = "C:\\Users\\Dania\\Desktop\\New folder (2)"

    start_freq, freq_num, freq_gap = 15450, 1, 0

    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    spectrum_output_path = "C:\\Users\\Dania\\Desktop\\New folder (2)"
    spectrum_output_file = os.path.join(spectrum_output_path, file_name + '_filtered' + '.csv')

    lowcut, highcut = start_freq - 550, 18010

    filtered_samples = butter_bandpass_filter(samples, lowcut, highcut, sampFreq, order=3)
    get_magnitude_spectrum(sampFreq, filtered_samples, 'linear', 'Filtered Signal Spectrum', True, spectrum_output_file)

    plot_signal(sampFreq, filtered_samples, file_name)

    show()
