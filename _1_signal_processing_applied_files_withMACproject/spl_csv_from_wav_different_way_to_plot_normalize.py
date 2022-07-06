import os
from tkinter import font

import pandas as pd
from pylab import *
from scipy.io import wavfile

from _0_signal_processing_functions.band_pass_filter import butter_bandpass_filter
from _0_signal_processing_functions.sound_pressure_level import write_csv_file, getOverlappedSampleAmplitude
from quantize_reconcile_amplify_privacy.quant_chunks import detect_step_in_time_series, extract_step_df
import matplotlib.pyplot as plt


def normalize(df, x, y):
    m = df.min()
    range = df.max() - m
    df_temp = (df - m) / range

    range2 = y - x
    df_norm = (df_temp * range2) + x

    return df_norm

def spl_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order, do_filter):
    concat_step_amp_Alice, concat_step_amp_Bob, concat_step_amp_Eve = list(), list(), list()
    output_path = input_path

    image_name3 = 'concat-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl-step'
    concat_step_amp = os.path.join(output_path, image_name3 + '.png')

    for num in range(1, numOfRounds + 1):

        image_name1 = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl'
        image_spl = os.path.join(output_path, image_name1 + '.png')

        image_name2 = str(num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-spl-step'
        image_spl_step = os.path.join(output_path, image_name2 + '.png')


        '''____________________ Alice ____________________'''

        file_name_Alice = str(num) + 'Alice' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
        input_file_Alice = os.path.join(input_path, file_name_Alice + '.wav')

        sampFreq_Alice, samples_Alice = wavfile.read(input_file_Alice)

        ## Filtering
        if(do_filter == 'True'):
            samples_Alice = butter_bandpass_filter(samples_Alice, lowcut, highcut, sampFreq_Alice, order=filter_order)

        ## Get SPL Values
        spl_list_Alice, spl_list_dB_Alice, time_list_Alice = getOverlappedSampleAmplitude(samples_Alice)
        spl_output_file_Alice = os.path.join(output_path, file_name_Alice + '.csv')
        write_csv_file(spl_output_file_Alice, spl_list_Alice, time_list_Alice)
        df_Alice = pd.read_csv(spl_output_file_Alice)

        ## Get SPL Values only at the Step
        step_index_Alice = detect_step_in_time_series(df_Alice)
        step_df_Alice = extract_step_df(df_Alice, step_index_Alice, 1000)

        concat_step_amp_Alice += step_df_Alice['Amp'].tolist()

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

        '''____________________ Plot SPL ____________________'''

        plt.figure()
        df_Alice_norm_amp = normalize(df_Alice['Amp'], 0, 20)
        df_Bob_norm_amp = normalize(df_Bob['Amp'], 0, 20)
        df_Eve_norm_amp = normalize(df_Eve['Amp'], 0, 20)

        plt.plot(df_Alice_norm_amp.reset_index(drop=True), color='darkred', label='Tx2 -> Rx2', linewidth=1.0, linestyle='-')
        plt.plot(df_Bob_norm_amp.reset_index(drop=True), color='darkblue', label='Rx2 -> Tx2', linewidth=1.0, linestyle='--')
        # plt.plot(df_Eve_norm_amp.reset_index(drop=True), color='forestgreen', label='A -> E', linewidth=1.0, linestyle='-.')

        plt.legend()
        plt.xlabel('Time [ms]')
        plt.ylabel('SPL [pascal]')
        plt.savefig(image_spl,  bbox_inches='tight')

        '''____________________ Plot step SPL ____________________'''

        # plt.figure()
        df_Alice_norm_amp_step = normalize(step_df_Alice['Amp'], 0, 20)
        df_Bob_norm_amp_step = normalize(step_df_Bob['Amp'], 0, 20)
        df_Eve_norm_amp_step = normalize(step_df_Eve['Amp'], 0, 20)

        # plt.plot(df_Alice_norm_amp_step.reset_index(drop=True), color='darkred', label='B -> A', linewidth=1.0, linestyle='-')
        # plt.plot(df_Bob_norm_amp_step.reset_index(drop=True), color='darkblue', label='A -> B', linewidth=1.0, linestyle='--')
        # plt.plot(df_Eve_norm_amp_step.reset_index(drop=True), color='forestgreen', label='A -> E', linewidth=1.0, linestyle='-.')

        ##-------------------------------------------------------------------------------------------------------------
        # Final_Shared_Key_Dec_AB_bit_string = '10001111101010100101000101110100001111111110001111010011011100110110101110111101001010010100010101000111010110101111110000011001'
        # Final_Shared_Key_Dec_AE_bit_string = '01101000001000101000010110000011111110101101011111101101011001000101111111010010001011101100101111011100111110011111100000101100'

        # Final_Shared_Key_Dec_AB = 240225049246642651722999240578559649321
        Final_Shared_Key_Dec_AB = 79791884210741572035837849920862200905

        Final_Shared_Key_Dec_AE = 102363648286154459468633706935384406060

        f2, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(df_Alice_norm_amp_step.reset_index(drop=True), color='darkred', label='Tx1 -> Rx1', linewidth=1.0, linestyle='-')
        ax1.plot(df_Bob_norm_amp_step.reset_index(drop=True), color='darkblue', label='Rx1 -> Tx1', linewidth=1.0, linestyle='--')
        # ax1.text(100, 0.5, r'Key obtained at ($A$,$B$) = %d' %Final_Shared_Key_Dec_AB, fontsize=7, fontweight='light')
        ax1.text(100, 0.5, r'$Key_{x1}$ = %d' %Final_Shared_Key_Dec_AB, fontsize=7, fontweight='light')


        ax2.plot(df_Alice_norm_amp_step.reset_index(drop=True), color='darkred', label='B -> A', linewidth=1.0, linestyle='-')
        # ax2.plot(df_Eve_norm_amp_step.reset_index(drop=True), color='forestgreen', label='A -> E', linewidth=1.0, linestyle='--')
        # ax2.text(100, 0.5, r'Key inferred at ($E$) = %d' %Final_Shared_Key_Dec_AE, fontsize=7, fontweight='light')
        #
        # ##-------------------------------------------------------------------------------------------------------------
        # ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #            ncol=2, mode="expand", borderaxespad=0.)
        # ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #            ncol=2, mode="expand", borderaxespad=0.)

        ax1.legend(loc=1)
        ax2.legend(loc=2)


        ax1.yaxis.set_ticks_position('both')
        ax2.yaxis.set_ticks_position('both')

        ax1.xaxis.set_ticks_position('both')
        ax2.xaxis.set_ticks_position('both')

        ax1.tick_params(direction='in')
        ax2.tick_params(direction='in')

        # ax2.text(0.05, 0.5, 'SPL [pascal]', va='center', rotation='vertical',  size=9)
        ax1.set_xlabel('Time [ms]')
        ax1.set_ylabel('SPL [pascal]')

        f2.savefig(image_spl_step,  bbox_inches='tight')

    '''____________________ Plot concatenated step SPL ____________________'''

    # plt.figure()
    # plt.plot(concat_step_amp_Alice, color='red', label='B -> A', linewidth=1.0, linestyle='-')
    # plt.plot(concat_step_amp_Bob, color='darkblue', label='A -> B', linewidth=1.0, linestyle='--')
    # plt.plot(concat_step_amp_Eve, color='forestgreen', label='A -> E', linewidth=1.0, linestyle='-.')
    #
    # plt.legend()
    # plt.xlabel('Time [ms]')
    # plt.ylabel('SPL [pascal]')
    # plt.savefig(concat_step_amp, bbox_inches='tight')

'''_____________________________________________________ Run _____________________________________________________'''

if (__name__) == "__main__":

    # input_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2-restudy"
    # start_freq, freq_num, freq_gap = 16000, 1, 0

    # input_path = "D:\\India-\\Ph.D\\5 project 2\\7-experiments\\4.1.gather projects-2devices"
    input_path = "D:\\India-\\Ph.D\\5 project 2\\7-experiments\\4.3.gather projects-4devices\\1stPair"
    # input_path = "D:\\India-\\Ph.D\\5 project 2\\7-experiments\\4.3.gather projects-4devices\\2ndPairData"

    start_freq, freq_num, freq_gap = 15450, 1, 0

    # lowcut, highcut = start_freq - 550, 18010

    lowcut, highcut = start_freq - 10, start_freq + ((freq_num - 1) * freq_gap) + 10
    filter_order = 3
    numOfRounds = 1
    do_filter ='True'

    spl_csv_from_wav(input_path, numOfRounds, start_freq, freq_num, freq_gap, lowcut, highcut, filter_order, do_filter)
    show()