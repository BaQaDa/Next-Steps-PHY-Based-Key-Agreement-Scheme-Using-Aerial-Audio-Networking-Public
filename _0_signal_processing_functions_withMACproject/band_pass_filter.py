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


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == '__main__':
    # file_name = '1-init-4000-15-250'
    #
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    file_name = "5Alice16000-1-0"
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\impTest"

    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    spectrum_output_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\spectrum_csv\\initiator_spectrum"
    spectrum_output_file = os.path.join(spectrum_output_path, file_name + '_filtered' + '.csv')

    start_freq, freq_num, freq_gap = 16000.0, 1, 0
    lowcut, highcut = start_freq - 5, start_freq + ((freq_num - 1) * freq_gap)

    filtered_samples = butter_bandpass_filter(samples, lowcut, highcut, sampFreq, order=3)
    get_magnitude_spectrum(sampFreq, filtered_samples, 'linear', 'Filtered Signal Spectrum', True, spectrum_output_file)

    show()