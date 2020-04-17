from quantize_reconcile_amplify_privacy.cascade import find_mismatch_num, bit_error_rate
from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from pylab import *
import os

if (__name__) == "__main__":
    # print('Enter your choice: 1 for KEY_AB, 2 for KEY_AC')
    # input1 = int(input())
    input1 = 1
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2"
    start_freq, freq_num, freq_gap = 16000, 1, 0
    first_file_num = 1
    last_file_num = first_file_num + 1

    output_path = input_path
    image_name1 = str(first_file_num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-numBits-Vs-chunkSize'
    image1 = os.path.join(output_path, image_name1 + '.png')

    image_name2 = str(first_file_num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap) + '-Pe-Vs-chunkSize'
    image2 = os.path.join(output_path, image_name2 + '.png')


    chunk_size_values = [i for i in np.arange(10, 100, 10)]
    Pe_values1 = list()
    num_bits_values = list()

    '''____________________ num_bits from quantization Vs. chunk_size (different alpha values) ____________________'''

    alpha_values = [i for i in np.arange(0.2, 1, 0.1)]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for alpha in alpha_values:
        for chunk_size in chunk_size_values:
            chunk_size, step_size, alpha = chunk_size, 1000, alpha

            cleaned_qts_resp, cleaned_qts_init = quantization(input_path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                                  step_size, chunk_size, alpha,
                                                                  start_freq, freq_num, freq_gap)
            num_bits = len(cleaned_qts_resp)
            num_bits_values.append(num_bits)

        plt.plot(chunk_size_values, num_bits_values, label=r'Value of $\alpha$ = %f' %alpha)
        plt.legend(loc=1)
        plt.xlabel('chunk-size')
        plt.ylabel('number of bits after quantization')
        plt.savefig(image1, bbox_inches='tight')
        num_bits_values.clear()

    # '''____________________ Pe vs. alpha (different chunk_size values) ____________________'''
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    #
    # for chunk_size in chunk_size_values:
    #     for alpha in alpha_values:
    #         chunk_size, step_size, alpha = chunk_size, 1000, alpha
    #         cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'Alice', 'Bob',
    #                                                           step_size, chunk_size, alpha,
    #                                                           start_freq, freq_num, freq_gap)
    #         Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
    #         Pe_values1.append(Pe)
    #
    #     ax.plot(alpha_values, Pe_values1, label='chunk_size = %d' %chunk_size )
    #     plt.legend(loc=2)
    #     plt.xlabel(r'Value of $\alpha$')
    #     plt.ylabel('Bit Mismatch Rate')
    #     Pe_values1.clear()

    '''____________________ Pe Vs. chunk_size (alpha values taken according to proper num-bits chosen from the upper plot ) ____________________'''

    # alpha_values = [i for i in np.arange(0.6, 0.75, 0.1)]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for alpha in alpha_values:
        for chunk_size in chunk_size_values:
            chunk_size, step_size, alpha = chunk_size, 1000, alpha

            cleaned_qts_resp, cleaned_qts_init = quantization(input_path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                                  step_size, chunk_size, alpha,
                                                                  start_freq, freq_num, freq_gap)
            Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
            Pe_values1.append(Pe)

        plt.plot(chunk_size_values, Pe_values1, label=r'Value of $\alpha$ = %f' %alpha)
        plt.legend(loc=3)
        plt.xlabel('chunk-size')
        plt.ylabel('Bit Mismatch Rate')
        plt.savefig(image2,  bbox_inches='tight')
        Pe_values1.clear()

    plt.show()
