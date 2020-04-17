import csv
import os

from matplotlib import ticker
from pylab import *
from scipy.io import wavfile

'''
For information about the function (magnitude_spectrum) usage, check: 
1.  https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.magnitude_spectrum.html
2.  https://kite.com/python/docs/matplotlib.mlab.magnitude_spectrum

@param 
    scale   is {'default', 'linear', 'dB'}
              The scaling of the values in the *spec*.  'linear' is no scaling.
              'dB' returns the values in dB scale, i.e., the dB amplitude
              (20 * log10). 'default' is 'linear'.
@:returns
    spectrum is 1-D array, the values for the magnitude spectrum before scaling (real valued).
    freqs    is 1-D array, the frequencies corresponding to the elements in *spectrum*.
'''


def get_magnitude_spectrum(sampFreq, samples, scale, plot_title, write_spectrum_csv, output_file):
    # plt.figure()
    # plt.xlim([10, sampFreq / 2])
    # plt.xscale('log')
    fig = plt.figure()
    fig.text(0.575, 0.045, '[KHz]', va='center', rotation='horizontal', size=10)
    ax = fig.add_subplot(111)
    scale_x = 1e3
    # locator = matplotlib.ticker.MaxNLocator(24)
    # ax.xaxis.set_major_locator(locator)
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:1n}'.format(x / scale_x))
    ax.xaxis.set_major_formatter(ticks_x)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(direction='in')
    spectrum, freqs, lines = magnitude_spectrum(samples, Fs=sampFreq, scale=scale, color='black')

    if write_spectrum_csv == True:
        if scale == 'dB':
            spectrum = 20. * np.log10(spectrum)
        elif scale == 'linear':
            spectrum = spectrum

        field_names = ['frequency', 'magnitude']

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
        f.close()

        rows = zip(freqs.tolist(), spectrum.tolist())

        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)


def check_noise_spectrum(num, input_path, party_name, start_freq, freq_num, freq_gap):

    file_name = str(num) + party_name + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    output_path = input_path
    spectrum_output_file = os.path.join(output_path, file_name + '.csv')

    get_magnitude_spectrum(sampFreq, samples, 'linear', 'Received Signal  Spectrum', True, spectrum_output_file)

    image_name = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-ambient-noise'
    image_spl_step = os.path.join(output_path, image_name + '.png')
    plt.savefig(image_spl_step, bbox_inches='tight')

'''_____________________________________________________ Run _____________________________________________________'''

if __name__ == '__main__':
    ## NOTES:

    '''In the conference room, I did not run any tone by any of the parties, files with (start_freq, freq_num, freq_gap = 0, 1, 0)'''

    '''In the conference room, alice sent tone  while Bob and Eve did not send tones, files with (start_freq, freq_num, freq_gap = 3000, 1, 0)
     , with high volume : files with (num = 1,2)
     with high volume : files with (num = 3,4)'''
    '''Change this number in file_name = str(num)'''

    start_freq, freq_num, freq_gap = 0, 1, 0
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\AmbientNoise"
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference"


    for i in range (1,4):

        check_noise_spectrum(i, input_path, 'Eve', start_freq, freq_num, freq_gap)
    show()
