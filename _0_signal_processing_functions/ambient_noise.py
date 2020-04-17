import csv
import os

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
    plt.figure(figsize=(6, 4))
    plt.xlim([10, sampFreq / 2])
    plt.xscale('log')
    plt.title(plot_title)
    spectrum, freqs, lines = magnitude_spectrum(samples, Fs=sampFreq, scale=scale)


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


if __name__ == '__main__':

    ## NOTES:

    '''In the conference room, I did not run any tone by any of the parties, files with (start_freq, freq_num, freq_gap = 0, 1, 0)'''

    '''In the conference room, alice sent tone  while Bob and Eve did not send tones, files with (start_freq, freq_num, freq_gap = 3000, 1, 0)
     , with high volume : files with (num = 1,2)
     with high volume : files with (num = 3,4)'''

    ##

    start_freq, freq_num, freq_gap = 3000, 1, 0
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\AmbientNoise"

    file_name= str(3) + 'Bob' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    output_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\spectrum_csv\\initiator_spectrum"
    spectrum_output_file = os.path.join(output_path, file_name + '.csv')

    get_magnitude_spectrum(sampFreq, samples, 'linear', 'Received Signal  Spectrum', True, spectrum_output_file)

    show()
