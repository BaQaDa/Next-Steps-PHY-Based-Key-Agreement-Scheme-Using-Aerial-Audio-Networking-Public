import os
import itertools
from pylab import *
from quantize_reconcile_amplify_privacy.cascade import bit_error_rate, setBasicBlockSize, output, cascade
from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from Generate_Key.run_file_get_keys import finalLength, _securityParameter

if (__name__) == "__main__":

    # input_path = "D:\\India-\\Ph.D\\3 project 1\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2-restudy"
    # start_freq, freq_num, freq_gap = 16000, 1, 0

    input_path = "C:\\Users\\Dania\\Desktop\\New folder (2)"
    start_freq, freq_num, freq_gap = 15450, 1, 0

    first_file_num = 1
    last_file_num = first_file_num + 1

    output_path = input_path
    image_name3 = str(first_file_num) + '-' + str(start_freq) + '-' + str(freq_num) + '-' + str(
        freq_gap) + '-KGR-BCR-Vs-chunkSize'
    image3 = os.path.join(output_path, image_name3 + '.png')

    chunk_size_values = [i for i in np.arange(5, 55, 5)]
    alpha_values = [i for i in np.arange(0.2, 1.0, 0.2)]
    marker = itertools.cycle(('.', 'h', 's', 'd'))
    Pe_values1 = list()
    num_bits_values = list()
    num_bits_rate = list()

    '''____________________ num_bits (length of the final key) Vs. chunk_size (at different alpha values) ____________________'''

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)


    ax1.yaxis.set_ticks_position('both')
    ax2.yaxis.set_ticks_position('both')

    ax1.xaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')

    ax1.set_ylabel('Key Generation Rate [bit/sec]')
    ax2.set_ylabel('Bit Conflict Rate')
    ax2.set_xlabel('chunk-size')

    ax1.tick_params(direction='in')
    ax2.tick_params(direction='in')

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

        ax1.plot(chunk_size_values, num_bits_rate, label=r'$\alpha$ = %.1f'%alpha, marker=next(marker))
        num_bits_values.clear()
        num_bits_rate.clear()


    '''____________________ Pe Vs. chunk_size (alpha values taken according to proper num-bits chosen from the upper plot ) ____________________'''


    for alpha in alpha_values:
        for chunk_size in chunk_size_values:
            chunk_size, step_size, alpha = chunk_size, 1000, alpha

            cleaned_qts_resp, cleaned_qts_init = quantization(input_path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                                  step_size, chunk_size, alpha,
                                                                  start_freq, freq_num, freq_gap)
            Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
            Pe_values1.append(Pe)

        ax2.plot(chunk_size_values, Pe_values1, label=r'$\alpha$ = %.1f' %alpha, marker=next(marker))
        Pe_values1.clear()

        '''____________________ Plot both in one window ____________________'''
    # ax1.legend(loc=2, fontsize=10)
    # ax2.legend(loc=2, fontsize=10)
    ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    fig.savefig(image3,  bbox_inches='tight')

    plt.show()
