import matplotlib.pyplot as plt
import numpy as np
import os

from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter
from pylab import *
from scipy.io import wavfile


# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\Novib"
input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\vib"
# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\moveObj"
# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\moveMob"


spl_output_path = input_path

start_freq, freq_num, freq_gap = 16500, 15, 250
lowcut, highcut = start_freq, start_freq + ((freq_num - 1) * freq_gap)
num =3

'''initiator'''

file_name1 = str(num) + '-init-16500-15-250'
input_file1 = os.path.join(input_path, file_name1 + '.wav')
sampFreq1, samples1 = wavfile.read(input_file1)
filtered_samples1 = butter_bandpass_filter(samples1, lowcut, highcut, sampFreq1, order=6)

'''2nd Party'''

file_name2 = str(num) + '-second-16500-15-250'
input_file2 = os.path.join(input_path, file_name2 + '.wav')
sampFreq2, samples2 = wavfile.read(input_file2)
filtered_samples2 = butter_bandpass_filter(samples2, lowcut, highcut, sampFreq2, order=6)

'''3rd Party'''

file_name3 = str(num) + '-secondC-16500-15-250'
input_file3 = os.path.join(input_path, file_name3 + '.wav')
sampFreq3, samples3 = wavfile.read(input_file3)
filtered_samples3 = butter_bandpass_filter(samples3, lowcut, highcut, sampFreq3, order=6)


fig = plt.figure()
plt.plot(np.correlate(filtered_samples1, filtered_samples2,"full"))
fig = plt.figure()
plt.plot(np.correlate(filtered_samples2, filtered_samples3,"full"))

plt.show()