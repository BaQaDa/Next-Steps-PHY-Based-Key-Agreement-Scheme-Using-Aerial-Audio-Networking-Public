import os
import pandas as pd
from pylab import *
from scipy.io import wavfile

from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter
from _0_signal_processing_functions.sound_pressure_level import write_csv_file, getOverlappedSampleAmplitude
from quantize_reconcile_amplify_privacy.quant_chunks import detect_step_in_time_series, extract_step_df
import matplotlib.pyplot as plt



def spl_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order, do_filter):
    concat_step_amp_Alice, concat_step_amp_Bob, concat_step_amp_Eve = list(), list(), list()
    output_path = input_path

    image_name3 = 'concat-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl-step.png'
    concat_step_amp = os.path.join(output_path, image_name3 + '.png')

    for num in range(1, numOfRounds + 1):

        image_name1 = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl.png'
        image_spl = os.path.join(output_path, image_name1 + '.png')

        image_name2 = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl-step.png'
        image_spl_step = os.path.join(output_path, image_name2 + '.png')

        image_name4 = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-room-range.png'
        image_room_range = os.path.join(output_path, image_name4 + '.png')

        '''____________________ Bob ____________________'''

        file_name_Bob = str(num) + 'Bob' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Bob = os.path.join(input_path, file_name_Bob + '.wav')

        sampFreq_Bob, samples_Bob = wavfile.read(input_file_Bob)

        ## Filtering
        if(do_filter == 'True'):
            samples_Bob = butter_bandpass_filter(samples_Bob, lowcut, highcut, sampFreq_Bob, order=filter_order)

        ## Get SPL Values
        spl_list_Bob, spl_list_dB_Bob, time_list_Bob = getOverlappedSampleAmplitude(samples_Bob)
        spl_output_file_Bob = os.path.join(output_path, file_name_Bob + '.csv')
        write_csv_file(spl_output_file_Bob, spl_list_Bob, time_list_Bob)
        df_Bob = pd.read_csv(spl_output_file_Bob)

        ## Get SPL Values only at the Step
        step_index_Bob = detect_step_in_time_series(df_Bob)
        step_df_Bob = extract_step_df(df_Bob, step_index_Bob, 1000)

        concat_step_amp_Bob += step_df_Bob['Amp'].tolist()

        '''____________________ Eve ____________________'''

        file_name_Eve = str(num) + 'Eve' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Eve = os.path.join(input_path, file_name_Eve + '.wav')

        sampFreq_Eve, samples_Eve = wavfile.read(input_file_Eve)

        ## Filtering
        if(do_filter == 'True'):
            samples_Eve = butter_bandpass_filter(samples_Eve, lowcut, highcut, sampFreq_Eve, order=filter_order)

        ## Get SPL Values
        spl_list_Eve, spl_list_dB_Eve, time_list_Eve = getOverlappedSampleAmplitude(samples_Eve)
        spl_output_file_Eve = os.path.join(output_path, file_name_Eve + '.csv')
        write_csv_file(spl_output_file_Eve, spl_list_Eve, time_list_Eve)
        df_Eve = pd.read_csv(spl_output_file_Eve)

        ## Get SPL Values only at the Step
        step_index_Eve = detect_step_in_time_series(df_Eve)
        step_df_Eve = extract_step_df(df_Eve, step_index_Eve, 1000)

        concat_step_amp_Eve += step_df_Eve['Amp'].tolist()

        '''____________________ Plot both receivers signals in one graph ____________________'''

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(df_Bob['Amp'], color='darkblue', label='inside room', linewidth=1.0)
        plt.plot(df_Eve['Amp'], color='forestgreen', label='outside room', linewidth=1.0, linestyle='--')
        plt.legend()
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        ax.tick_params(direction='in')
        plt.xlabel('Time [msec]')
        plt.ylabel('SPL [pascal]')
        plt.savefig(image_room_range,  bbox_inches='tight')

    #     '''____________________ Plot SPL ____________________'''
    #
    #     f1, (ax2, ax3) = plt.subplots(2, 1, sharex=True)
    #     f1.subplots_adjust(hspace=0.3)
    #
    #     ax2.plot(df_Bob['Time'], df_Bob['Amp'], color='black', linewidth=1.0)
    #     ax3.plot(df_Eve['Time'], df_Eve['Amp'], color='black', linewidth=1.0)
    #
    #     ax2.set_title("Alice -> Bob")
    #     ax3.set_title("Alice -> Eve")
    #
    #     ax2.grid(True)
    #     ax3.grid(True)
    #
    #     f1.text(0.04, 0.5, 'SPL [pascal]', va='center', rotation='vertical')
    #     ax3.set_xlabel('Time [ms]')
    #     plt.savefig(image_spl,  bbox_inches='tight')
    #
    #
    #     '''____________________ Plot step SPL ____________________'''
    #
    #     f2, (ax2, ax3) = plt.subplots(2, 1, sharex=True)
    #     f2.subplots_adjust(hspace=0.3)
    #
    #     ax2.plot(step_df_Bob['Time'], step_df_Bob['Amp'], color='black', linewidth=1.0)
    #     ax3.plot(step_df_Eve['Time'], step_df_Eve['Amp'], color='black', linewidth=1.0)
    #
    #     ax2.set_title("Alice -> Bob")
    #     ax3.set_title("Alice -> Eve")
    #
    #     ax2.grid(True)
    #     ax3.grid(True)
    #
    #     f2.text(0.04, 0.5, 'SPL [pascal]', va='center', rotation='vertical')
    #     ax3.set_xlabel('Time [ms]')
    #     plt.savefig(image_spl_step,  bbox_inches='tight')
    #     # plt.show()
    #
    # '''____________________ Plot concatenated step SPL ____________________'''
    #
    #
    # f2, (ax2, ax3) = plt.subplots(2, 1, sharex=True)
    # f2.subplots_adjust(hspace=0.3)
    #
    # ax2.plot(concat_step_amp_Bob, color='black', linewidth=1.0)
    # ax3.plot(concat_step_amp_Eve, color='black', linewidth=1.0)
    #
    # ax2.set_title("Bob -> Alice")
    # ax3.set_title("Alice -> Eve")
    #
    # ax2.grid(True)
    # ax3.grid(True)
    #
    # f2.text(0.04, 0.5, 'SPL [pascal]', va='center', rotation='vertical')
    # ax3.set_xlabel('Time [ms]')
    # plt.savefig(concat_step_amp, bbox_inches='tight')
    # plt.show()

'''_____________________________________________________ Run _____________________________________________________'''

if (__name__) == "__main__":
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference"
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Corridor"
    input_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\Exps_paper\\Locality"
    # input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\room-multi-freq"

    start_freq, freq_num, freq_gap = 16000, 1, 0
    lowcut, highcut = start_freq - 10, start_freq + ((freq_num - 1) * freq_gap) + 10
    filter_order = 2
    numOfRounds = 4
    do_filter ='True'

    spl_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order, do_filter)