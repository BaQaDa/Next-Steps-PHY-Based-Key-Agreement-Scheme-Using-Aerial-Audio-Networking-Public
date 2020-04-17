import os

from matplotlib import ticker
from pylab import *
from scipy.fftpack import fft,fftfreq
import matplotlib.pyplot as plt

from scipy.io import wavfile
from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter




if __name__ == '__main__':

    file_name = '1Alice16000-15-250'

    '''Original Received Signal
       ------------------------'''
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\16000-room-2000amp"
    input_file = os.path.join(input_path, file_name + '.wav')
    output_path = input_path

    samplerate, data1 = wavfile.read(input_file)

    start_freq, freq_num, freq_gap = 16000, 15, 250
    lowcut, highcut = start_freq - 10, start_freq + ((freq_num - 1) * freq_gap) + 10
    filter_order = 4
    numOfRounds = 2
    data = butter_bandpass_filter(data1, lowcut, highcut, samplerate, order=filter_order)
    num_samples = data.shape[0]
    datafft = fft(data)
    # Get the absolute value of real and complex component:
    fftabs = abs(datafft)

    import matplotlib.pyplot as plt
    from scipy.misc import electrocardiogram
    from scipy.signal import find_peaks

    x = fftabs
    peaks, _ = find_peaks(x, height=0.5)
    plt.plot(x)
    plt.plot(peaks, x[peaks], "x")
    plt.plot(np.zeros_like(x), "--", color="gray")
    plt.show()

    print(type(fftabs))
    freqs = fftfreq(num_samples, 1 / samplerate)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scale_x = 1e3
    # locator = matplotlib.ticker.MaxNLocator(24)
    # ax.xaxis.set_major_locator(locator)
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:1n}'.format(x / scale_x))
    ax.xaxis.set_major_formatter(ticks_x)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(direction='in')
    # plt.xlim([10, samplerate / 2])
    # plt.xscale('log')
    # plt.grid(True)
    plt.xlabel('Frequency [KHz]')
    plt.plot(freqs[:int(freqs.size / 2)], fftabs[:int(freqs.size / 2)]/1e4)
    plt.show()