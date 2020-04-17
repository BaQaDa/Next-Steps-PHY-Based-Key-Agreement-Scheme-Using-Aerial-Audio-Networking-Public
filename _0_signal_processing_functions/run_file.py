import os

from pylab import *
from scipy.io import wavfile

from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter
from _0_signal_processing_functions.plot_get_magnitude_spectrum import get_magnitude_spectrum
from _0_signal_processing_functions.plot_signal import plot_signal
from _0_signal_processing_functions.sound_finder import remove_detected_silence

if __name__ == '__main__':

    file_name = '1-init-16000-15-250'

    '''Original Received Signal
       ------------------------'''
    "D:\India-\Ph.D\3 project 1\3rd sem\projects1\python\input_output_files\recordings\initiator"
    input_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)
    plot_signal(sampFreq, samples, 'Received Signal')

    '''Remove Silence
       --------------'''
    # sound_output_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\sound_only\\initiator_sound"
    # sound_output_file = os.path.join(sound_output_path, file_name + '.wav')
    #
    # # apply silence removing and write the sound into the output file
    # remove_detected_silence(input_file, sound_output_file, -50)
    #
    # # now, we can deal with and process the resultant sound file
    # sampFreq, samples = wavfile.read(sound_output_file)
    # plot_signal(sampFreq, samples, 'Received Sound Signal')

    '''Spectrum Before Filtering
       -------------------------'''

    spectrum_output_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\input_output_files\\spectrum_csv\\initiator_spectrum"
    spectrum_output_file = os.path.join(spectrum_output_path, file_name + '_filtered' + '.csv')
    get_magnitude_spectrum(sampFreq, samples, 'linear', 'Received Signal  Spectrum', True, spectrum_output_file)

    '''BPF Filtering
       -------------'''
    start_freq, freq_num, freq_gap = 16000.0, 15, 250
    lowcut, highcut = start_freq - 5, start_freq + ((freq_num - 1) * freq_gap)
    filtered_samples = butter_bandpass_filter(samples, lowcut, highcut, sampFreq, order=6)

    '''Spectrum After Filtering
       ------------------------'''
    # get_magnitude_spectrum(sampFreq, filtered_samples, 'linear', 'Filtered Signal Spectrum', True, spectrum_output_file)
    get_magnitude_spectrum(sampFreq, filtered_samples, 'linear', 'Filtered Signal Spectrum', True, spectrum_output_file)


    show()
