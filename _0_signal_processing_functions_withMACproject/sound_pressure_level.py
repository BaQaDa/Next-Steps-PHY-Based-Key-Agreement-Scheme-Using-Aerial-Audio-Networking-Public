import os
import csv

from pylab import *
from scipy.io import wavfile

'''
Get sound pressure Level (SPL) values over blocks of the samples:
To refine the graph, we need smaller window, so we take bufferSize = 512,
corresponds to sampling Window= 512/44.1= 11.6 ms.
So SPL value is computed once at each 11.6 ms Still for more refining,
we try to compute spl value at each 1 ms, for that we need to shift the
window by 1 ms, corresponds to shifting the buffer by size= 45
'''


def getOverlappedSampleAmplitude(samples):
    spl_list = list()
    spl_list_dB = list()
    time_list = list()

    val = 1
    i = 0
    while i < (len(samples) - 512):
        x = 0
        j = i
        temp = [0 for i in range(0, 512)]
        while j < (512 + i):
            temp.append(samples[j])
            x += 1
            j += 1
        buffer_spl, buffer_spl_dB = getAmplitude(temp)
        spl_list.append(buffer_spl)
        spl_list_dB.append(buffer_spl_dB)

        val = val + 1
        time_list.append(val)
        i += 45
        temp.clear()
    return spl_list, spl_list_dB, time_list


## Get Amplitude from one block
def getAmplitude(buffer):
    buffer_spl = sqrt(mean(np.power(buffer, 2)))
    buffer_spl_dB = 20.0 * np.log10(buffer_spl / (2 * 10e-5))
    # return buffer_spl_dB
    return buffer_spl, buffer_spl_dB


'''Get sound pressure Level (SPL) values over all samples'''


def spl_from_amplitude(samples, scale):
    spl_list = [np.sqrt(sample ** 2 / 2) for sample in samples]
    if scale == 'dB':
        spl_list = [20.0 * np.log10(spl_value / (2 * 10e-5)) for spl_value in spl_list]
    elif scale == 'pascal':
        spl_list == spl_list

    time_list = [i for i in range(1, len(samples) + 1)]
    return spl_list, time_list, scale


def spl_time_plot(spl_list, time_list, scale, plot_title):
    plt.figure(figsize=(6, 4))
    plt.plot(time_list, spl_list)
    plt.title(plot_title)
    plt.xlabel('Time [ms]')
    plt.ylabel('SPL = RSS [%s]' % scale)


def write_csv_file(output_file, spl_list, time_list):
    field_names = ['Time', 'Amp']

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(field_names)
    f.close()

    rows = zip(time_list, spl_list)

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    file_name = '1-init-4000-15-250'

    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)

    spl_list, time_list, scale = spl_from_amplitude(samples, 'pascal')
    spl_time_plot(spl_list, time_list, scale, 'SPL of Received Signal')
    show()
