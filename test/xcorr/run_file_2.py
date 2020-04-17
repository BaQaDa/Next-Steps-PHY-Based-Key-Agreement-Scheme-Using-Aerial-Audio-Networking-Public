import os
import pandas as pd
from pylab import *
from scipy.io import wavfile

from signal_processing_functions.band_pass_filter import butter_bandpass_filter
from signal_processing_functions.plot_get_magnitude_spectrum import get_magnitude_spectrum
from signal_processing_functions.plot_signal import plot_signal
from signal_processing_functions.sound_pressure_level import write_csv_file, getOverlappedSampleAmplitude
from quantize_reconcile_amplify_privacy.quant_chunks import detect_step_in_time_series, extract_step_df
import matplotlib.pyplot as plt

# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\Novib"
# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\vib"
input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\moveObj"
# input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\moveMob"


spl_output_path = input_path


start_freq, freq_num, freq_gap = 16500, 15, 250
lowcut, highcut = start_freq, start_freq + ((freq_num - 1) * freq_gap)

num = 3


'''---------------------------------------------------------------------------initiator'''

file_name1 = str(num) + '-init-16500-15-250'
input_file1 = os.path.join(input_path, file_name1 + '.wav')

sampFreq1, samples1 = wavfile.read(input_file1)
# plot_signal(sampFreq1, samples1, 'Initiator Received Signal')
filtered_samples1 = butter_bandpass_filter(samples1, lowcut, highcut, sampFreq1, order=6)
# plot_signal(sampFreq1, filtered_samples1, 'Initiator Received Signal')

spl_list1, spl_list_dB1, time_list1 = getOverlappedSampleAmplitude(filtered_samples1)
# spl_time_plot(spl_list1, time_list1, 'linear', 'SPL of Received Signal')
plt.figure(1)
plt.subplot(3, 1, 1)
plt.plot(time_list1, spl_list1)
plt.grid(True)
spl_output_file1 = os.path.join(spl_output_path, file_name1 + '.csv')
write_csv_file(spl_output_file1, spl_list1, time_list1)
df = pd.read_csv(spl_output_file1)
step_index = detect_step_in_time_series(df)
step_df = extract_step_df(df, step_index, 1000)
plt.figure(2)
plt.subplot(3, 1, 1)
plt.plot(step_df['Time'], step_df['Amp'])
plt.grid(True)

'''---------------------------------------------------------------------------2nd Party'''

file_name2 = str(num) + '-second-16500-15-250'
input_file2 = os.path.join(input_path, file_name2 + '.wav')
sampFreq2, samples2 = wavfile.read(input_file2)
# plot_signal(sampFreq1, samples1, 'Initiator Received Signal')
filtered_samples2 = butter_bandpass_filter(samples2, lowcut, highcut, sampFreq2, order=6)
# plot_signal(sampFreq2, filtered_samples2, '2nd Party Received Signal')

spl_list2, spl_list_dB2, time_list2= getOverlappedSampleAmplitude(filtered_samples2)

# spl_time_plot(spl_list2, time_list2, 'linear', 'SPL of Received Signal')
plt.figure(1)
plt.subplot(3, 1, 2)
plt.plot(time_list2, spl_list2)
plt.grid(True)
spl_output_file2 = os.path.join(spl_output_path, file_name2 + '.csv')
write_csv_file(spl_output_file2, spl_list2, time_list2)

df2 = pd.read_csv(spl_output_file2)
step_index2 = detect_step_in_time_series(df2)
step_df2= extract_step_df(df2, step_index2, 1000)
plt.figure(2)
plt.subplot(3, 1, 2)
plt.plot(step_df2['Time'], step_df2['Amp'])
plt.grid(True)

'''---------------------------------------------------------------------------3rd Party'''

file_name3 = str(num) + '-secondC-16500-15-250'
input_file3 = os.path.join(input_path, file_name3 + '.wav')
sampFreq3, samples3 = wavfile.read(input_file3)
# plot_signal(sampFreq3, samples3, 'Initiator Received Signal')
filtered_samples3 = butter_bandpass_filter(samples3, lowcut, highcut, sampFreq3, order=6)
# plot_signal(sampFreq3, filtered_samples3, '3rd Party Received Signal')

spl_list3, spl_list_dB3, time_list3 = getOverlappedSampleAmplitude(filtered_samples3)
# spl_time_plot(spl_list3, time_list3, 'linear', 'SPL of Received Signal')
plt.figure(1)
plt.subplot(3, 1, 3)
plt.plot(time_list3, spl_list3)
plt.grid(True)
spl_output_file3 = os.path.join(spl_output_path, file_name3 + '.csv')
write_csv_file(spl_output_file3, spl_list3, time_list3)

df3 = pd.read_csv(spl_output_file3)
step_index3 = detect_step_in_time_series(df3)
step_df3= extract_step_df(df3, step_index3, 1000)
plt.figure(2)
plt.subplot(3, 1, 3)
plt.plot(step_df3['Time'], step_df3['Amp'])
plt.grid(True)
plt.tight_layout()

'''---------------------------------------------------------------------------correlation'''

# plt.figure()
# plt.subplot(2,1,1)
# abba = np.correlate(filtered_samples1, filtered_samples2,"full")
# max_abba = np.max(abba)
# print(max_abba)
# time1 = arange(0, len(abba))
# plt.plot(time1, abba)
# plt.subplot(2,1,2)
# abac = np.correlate(
#
# , filtered_samples3,"full")
# max_abac = np.max(abac)
# print(max_abac)
# time2 = arange(0, len(abac))
# plt.plot(time2, abac)
#
#
# if(max_abba > max_abac):
#     print("max_abba > max_abac  !!!!!!!!!!!")
# else:
#     print("Noooooooooooooo")
plt.show()
