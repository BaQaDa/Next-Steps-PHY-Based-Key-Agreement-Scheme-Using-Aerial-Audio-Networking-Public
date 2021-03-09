import os
import itertools
from pylab import *
from quantize_reconcile_amplify_privacy.cascade import bit_error_rate, setBasicBlockSize, output, cascade
from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from Generate_Key.run_file_get_keys import finalLength, _securityParameter

if (__name__) == "__main__":

    input1 = 1
    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2"
    start_freq, freq_num, freq_gap = 16000, 1, 0
    first_file_num = 1
    last_file_num = first_file_num + 1

    output_path = input_path
    image_name1 = str(first_file_num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(
        freq_gap) + '-finalLength-Vs-chunkSize'
    image1 = os.path.join(output_path, image_name1 + '.png')

    image_name2 = str(first_file_num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(
        freq_gap) + '-Pe-Vs-chunkSize'
    image2 = os.path.join(output_path, image_name2 + '.png')

    chunk_size_values = [i for i in np.arange(5, 55, 5)]
    alpha_values = [i for i in np.arange(0.2, 1.0, 0.2)]
    marker = itertools.cycle(('.', '^', 'h', 's', 'd'))
    Pe_values1 = list()
    num_bits_values = list()
    num_bits_rate = list()

    '''____________________ num_bits (length of the final key) Vs. chunk_size (at different alpha values) ____________________'''


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(direction='in')
    round_num = 0
    for alpha in alpha_values:
        round_num += 1
        print("\n********* Round_Num = ", round_num, "********* alpha = ", alpha, "*********")

        for chunk_size in chunk_size_values:
            print("chunk_size = ", chunk_size)
            chunk_size, step_size, alpha = chunk_size, 1000, alpha

            cleaned_qts_resp, cleaned_qts_init = quantization(input_path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                                  step_size, chunk_size, alpha,
                                                                  start_freq, freq_num, freq_gap)

            Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
            size = setBasicBlockSize(Pe)

            try:
                cascade(cleaned_qts_init, cleaned_qts_resp, size, 4)
            except IOError:
                print("Sorry ! cascade error ")
                print('alpha = ', alpha, 'chunk_size = ', chunk_size)

            Initial_Shared_Key, _totalDisclosedBits = output()
            _finalLength = finalLength(len(Initial_Shared_Key), _totalDisclosedBits, _securityParameter)
            num_bits_values.append(_finalLength)
            ## for KGR (num_bits_rate.append(_finalLength/(5500 * 1e-3))) check document [variables/points.docx]
            num_bits_rate.append(_finalLength/((5500 * 1e-3) + 0.3))

        plt.plot(chunk_size_values, num_bits_rate, label=r'$\alpha$ = %.1f'%alpha, marker=next(marker))
        plt.legend( fontsize=10)
        plt.xlabel('chunk-size')
        plt.ylabel('Key Generation Rate [bit/sec]')
        plt.savefig(image1, bbox_inches='tight')
        num_bits_values.clear()
        num_bits_rate.clear()

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

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(direction='in')
    for alpha in alpha_values:
        for chunk_size in chunk_size_values:
            chunk_size, step_size, alpha = chunk_size, 1000, alpha

            cleaned_qts_resp, cleaned_qts_init = quantization(input_path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                                  step_size, chunk_size, alpha,
                                                                  start_freq, freq_num, freq_gap)
            Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
            Pe_values1.append(Pe)

        plt.plot(chunk_size_values, Pe_values1, label=r'$\alpha$ = %.1f' %alpha, marker=next(marker))
        plt.legend(fontsize=10)
        plt.xlabel('chunk-size')
        plt.ylabel('Bit Conflict Rate')
        plt.savefig(image2,  bbox_inches='tight')
        Pe_values1.clear()

    plt.show()
