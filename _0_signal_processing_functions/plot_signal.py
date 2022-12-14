import os

from pylab import *
from scipy.io import wavfile

''' 
Time Representation of the sound can be obtained by plotting the pressure
values against the time axis. we create an array containing the time points first 
'''


def plot_signal(samplerate, samples, plot_title):
    timeArray = arange(0, len(samples), 1)
    timeArray = timeArray / samplerate
    timeArray = timeArray * 1000  # scale to milliseconds
    plt.figure(figsize=(6, 4))
    plt.plot(timeArray, samples, 'y')
    plt.grid(True)
    plt.title(plot_title)
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude')


if __name__ == '__main__':
    file_name = '1-init-4000-15-250'

    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    input_file = os.path.join(input_path, file_name + '.wav')

    sampFreq, samples = wavfile.read(input_file)
    plot_signal(sampFreq, samples, 'Received Signal')


    show()
