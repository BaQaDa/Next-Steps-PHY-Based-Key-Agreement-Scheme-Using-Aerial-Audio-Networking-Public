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
    # file_name = '1-init-4000-15-250'
    file_name = "1Alice15450-1-0"

    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\impTest"
    input_path = "C:\\Users\\Dania\\Desktop\\New folder (2)"
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    spectrum_output_path =  "C:\\Users\\Dania\\Desktop\\New folder (2)"
    spectrum_output_file = os.path.join(spectrum_output_path, file_name + '.csv')

    get_magnitude_spectrum(sampFreq, samples, 'linear', 'Received Signal  Spectrum', True, spectrum_output_file)

    show()
