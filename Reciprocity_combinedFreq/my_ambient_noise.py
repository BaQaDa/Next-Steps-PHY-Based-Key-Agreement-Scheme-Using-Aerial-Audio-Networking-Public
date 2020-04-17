import os

from matplotlib import ticker
from pylab import *
from scipy.fftpack import fft,fftfreq
import matplotlib.pyplot as plt
from scipy.io import wavfile

def normalize(array, x, y):
    m = array.min()
    range = array.max() - m
    array_temp = (array - m) / range
    range2 = y - x
    array_norm = (array_temp * range2) + x
    return array_norm

if __name__ == '__main__':

    file_name = '2Eve0-1-0'

    '''Original Received Signal
       ------------------------'''
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Used_AmbientNoise-My Spectrum function"
    input_file = os.path.join(input_path, file_name + '.wav')
    output_path = input_path

    samplerate, data = wavfile.read(input_file)
    start_freq, freq_num, freq_gap = 0, 1, 0



    samples = data.shape[0]

    datafft = fft(data)
    # Get the absolute value of real and complex component:
    fftabs = abs(datafft)
    fftabs_norm = normalize(fftabs, 0, 60)

    freqs = fftfreq(samples, 1 / samplerate)
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
    plt.ylabel('Magnitude (energy)')
    plt.plot(freqs[:int(freqs.size / 2)], fftabs_norm[:int(freqs.size / 2)], color='black')
    image_name = str(2) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-ambient-noise'
    image_spl_step = os.path.join(output_path, image_name + '.png')
    plt.savefig(image_spl_step, bbox_inches='tight')
    plt.show()

